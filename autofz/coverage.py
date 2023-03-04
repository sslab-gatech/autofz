#!/usr/bin/env python3
'''
1. create a docker instance for each fuzzer
'''
import json
import logging
import os
import re
from typing import Dict, Optional

import filelock

from . import config as Config
from . import evaluator
from .datatype import Bitmap

config = Config.CONFIG

logger = logging.getLogger('autofz.coverage')

EVALUTOR_THREAD = None


def parse_afl_cov_output(output):
    m_line = re.search(
        r'lines\.\.\.\.\.\.: (\d*\.\d+|\d+)% \((\d+) of (\d+) lines\)', output)
    m_function = re.search(
        r'functions\.\.: (\d*\.\d+|\d+)% \((\d+) of (\d+) functions\)', output)
    line_coverage = None
    line = None
    line_total = None
    function_coverage = None
    function = None
    function_total = None
    if m_line and len(m_line.groups()) == 3:
        line_coverage = float(m_line.group(1))
        line = int(m_line.group(2))
        line_total = int(m_line.group(3))
    if m_function and len(m_function.groups()) == 3:
        function_coverage = float(m_function.group(1))
        function = int(m_function.group(2))
        function_total = int(m_function.group(3))
    ret = {
        'line_coverage': line_coverage,
        'line': line,
        'line_total': line_total,
        'function_coverage': function_coverage,
        'function': function,
        'function_total': function_total
    }
    return ret


def get_bitmap_fuzzer(target, fuzzer, output_dir):
    fuzzer_output_dir = os.path.join(output_dir, 'eval', fuzzer)
    lock_path = os.path.realpath(os.path.join(output_dir, 'eval', 'lock'))
    if not os.path.exists(lock_path): return None
    bitmap_path = os.path.join(fuzzer_output_dir, 'bitmap')
    lock = filelock.FileLock(lock_path, timeout=300)
    bitmap = None
    with lock:
        if not os.path.exists(bitmap_path):
            logger.critical(f'{bitmap_path} is None')
            return None
        if os.path.exists(bitmap_path):
            bitmap = Bitmap(bitmap_path=bitmap_path)
    assert bitmap
    return bitmap


def get_coverage_global(output_dir):
    global_output_dir = os.path.join(output_dir)
    log_path = os.path.realpath(
        os.path.join(global_output_dir, 'cov', 'afl-cov-latest.log'))
    if not os.path.exists(log_path):
        return None
    with open(log_path, 'r') as f:
        afl_cov_output = f.read()
    coverage = parse_afl_cov_output(afl_cov_output)
    return coverage


def get_unique_bugs_fuzzer(target, fuzzer, output_dir):
    fuzzer_output_dir = os.path.join(output_dir, 'eval', fuzzer)
    lock_path = os.path.realpath(os.path.join(output_dir, 'eval', 'lock'))
    lock = filelock.FileLock(lock_path, timeout=300)
    if not os.path.exists(lock_path): return None
    log_path = os.path.join(fuzzer_output_dir, 'crashrunner-latest.log')
    log_new_path = os.path.join(fuzzer_output_dir,
                                'crashrunner-new-latest.json')
    unique_bugs = 0
    with lock:
        if not os.path.exists(log_new_path):
            logger.critical(f'{log_new_path} does not exist')
            return {
                "unique_bugs": 0,
                "unique_bugs_ip": 0,
                "unique_bugs_trace": 0,
                "unique_bugs_trace3": 0
            }
        with open(log_new_path, 'r') as f:
            data = json.load(f)
            # print(data)
            unique_bugs = data["unique_bugs"]
            unique_bugs_ip = data["unique_bugs_ip"]
            unique_bugs_trace = data["unique_bugs_trace"]
            unique_bugs_trace3 = data["unique_bugs_trace3"]
            return data
    # should not happen
    return {
        "unique_bugs": 0,
        "unique_bugs_ip": 0,
        "unique_bugs_trace": 0,
        "unique_bugs_trace3": 0
    }


def gen_evaluator_args(target,
                       fuzzers,
                       output_dir,
                       timeout,
                       input_dir=None,
                       empty_seed=False,
                       crash_mode='ip',
                       input_only=False):

    target_config = config['target'][target]
    evaluator_config: Dict[str, str] = config['evaluator']

    assert target_config

    group: str = target_config['group']
    target_default_args: str = target_config['args']['default']
    target_args = target_config['args'].get('evaluator', target_default_args)

    assert target_args is not None

    seed = None
    if input_dir:
        seed = input_dir
    elif empty_seed:
        seed = '/seeds/custom/empty'
    else:
        seed = target_config['seed']

    assert seed

    binary = os.path.join(evaluator_config['binary_root'], group, target,
                          target)
    binary_crash = os.path.join(evaluator_config['binary_crash_root'], group,
                                target, target)

    assert os.path.exists(seed)
    assert os.path.exists(binary)
    assert os.path.exists(binary_crash)

    evaluator_args = [
        '-o', output_dir, '-t', target, '-f', *fuzzers, '-q', 'queue', '-c',
        'crashes', '-T', timeout, '--input', seed, '--binary', binary,
        '--binary_crash', binary_crash, f'--args={target_args}', '--mode',
        crash_mode, '--live', '--sleep', 10
    ]
    if input_only:
        evaluator_args.append('--input-only')

    return list(map(str, evaluator_args))


def run_evaluator(target, fuzzers, output_dir, timeout, input_dir, empty_seed,
                  crash_mode, input_only):
    evaluator_args = gen_evaluator_args(target, fuzzers, output_dir, timeout,
                                        input_dir, empty_seed, crash_mode,
                                        input_only)
    thread_evaluator = evaluator.main(evaluator_args)
    return thread_evaluator


def thread_run_evaluator(target, fuzzers, output_dir, timeout, input_dir,
                         empty_seed, crash_mode, input_only):
    global EVALUTOR_THREAD
    if EVALUTOR_THREAD: return
    thread_evaluator = run_evaluator(target, fuzzers, output_dir, timeout,
                                     input_dir, empty_seed, crash_mode,
                                     input_only)

    EVALUTOR_THREAD = thread_evaluator


def thread_run_fuzzer(target,
                      fuzzer,
                      fuzzers,
                      output_dir,
                      fuzzer_timeout='24h',
                      timeout='10s',
                      input_dir=None,
                      empty_seed=False,
                      crash_mode='trace',
                      input_only=False) -> Optional[Dict]:

    thread_run_evaluator(target, fuzzers, output_dir, timeout, input_dir,
                         empty_seed, crash_mode, input_only)
    bitmap = get_bitmap_fuzzer(target, fuzzer, output_dir)
    unique_bugs = get_unique_bugs_fuzzer(target, fuzzer, output_dir)
    # print('fuzzer', fuzzer, 'coverage', coverage)
    if bitmap:
        bitmap_count = bitmap.count()
        logger.debug(
            f'{target}, {fuzzer}, bitmap: {bitmap_count}, bugs: {unique_bugs}')
        return {
            # FIXME
            'coverage': {
                "line": 0,
                "line_coverage": 0
            },
            'bitmap': bitmap,
            'unique_bugs': unique_bugs
        }
    else:
        if not bitmap:
            logger.critical(f'{fuzzer} bitmap is None')
        return None


def thread_run_global(target,
                      fuzzers,
                      output_dir,
                      fuzzer_timeout='24h',
                      timeout='10s',
                      input_dir=None,
                      empty_seed=False,
                      crash_mode='trace',
                      input_only=False):
    result = thread_run_fuzzer(target, 'global', fuzzers, output_dir,
                               fuzzer_timeout, timeout, input_dir, empty_seed,
                               crash_mode, input_only)
    cov = get_coverage_global(output_dir)
    if not result:
        logger.critical(f'global bitmap is None')
        return None
    if cov:
        # NOTE: still return default 0, not waste time on line coverage
        result['coverage'] = cov
    else:
        logger.debug(f'global line cov is None')
    return result


def sync():
    evaluator.sync()
