#!/usr/bin/env python3
import copy
import ctypes
import glob
import hashlib
import json
import logging
import os
import pathlib
import random
import signal
import subprocess
import sys
import threading
import time
from enum import Enum
from multiprocessing import Pipe, Process, Queue
from pathlib import Path
from shutil import copy2
from typing import Any, Dict, List, Optional, Set, Tuple

import filelock
import numpy as np
from tap import Tap

from . import config as Config
from . import utils, watcher
from .common import IS_DEBUG
from .mytype import Fuzzer, Fuzzers, FuzzerType, SeedType

config = Config.CONFIG


class ArgsParser(Tap):
    output: Path
    target: str
    fuzzers: List[Fuzzer]
    queue_dir: Path
    crash_case_dir: Path
    binary: str
    binary_crash: str
    args: str
    live: bool
    sleep: int
    timeout: str
    mode: str
    input: str
    input_only: bool

    def configure(self):
        self.add_argument("-o",
                          "--output",
                          help="An output directory",
                          required=True)
        self.add_argument("-t", "--target", type=str, required=True)
        self.add_argument("-f", "--fuzzers", type=str, nargs='+')
        self.add_argument("-q",
                          "--queue-dir",
                          type=str,
                          help="test case dir",
                          default='queue')
        self.add_argument("-c",
                          "--crash-case-dir",
                          type=str,
                          help="crash case dir",
                          default='crashes')
        self.add_argument("--binary",
                          type=str,
                          help="coverage binary",
                          required=True)
        self.add_argument("--binary_crash",
                          type=str,
                          help="crash binary",
                          required=True)
        self.add_argument("--args", type=str, help="argument", default="")
        self.add_argument("--live", action='store_true', default=False)
        self.add_argument(
            "--sleep",
            type=int,
            help=
            "In --live mode, # of seconds to sleep between checking for new queue files",
            default=10)
        self.add_argument("-T",
                          "--timeout",
                          type=str,
                          help="timeout (default 10s)",
                          default='10s')
        self.add_argument("-m",
                          "--mode",
                          type=str,
                          choices=['trace', 'ip'],
                          required=True)
        self.add_argument("-i",
                          "--input",
                          type=str,
                          help="seed directory",
                          required=True)
        self.add_argument("--input-only",
                          help="Only evalaute seeds",
                          action="store_true",
                          default=False)


# random path to allow multiple exeuction of autofz
COVERAGE_LOCK_PATH: str = os.path.join(
    '/tmp', 'coverage_lock_' + utils.get_random_string(10))
COVERAGE_LOCK = filelock.FileLock(COVERAGE_LOCK_PATH, timeout=100)

ARGS: ArgsParser

FUZZERS: Fuzzers

LAST_INDEX: Dict[watcher.Watcher, int] = {}

MAP = {}

# FUNCTION #### SOURCE_FILE #### frame number
ASAN_OPTIONS = 'stack_trace_format="####%p####%f####%S####%n####"'

INDEX = {}
INDEX_UNIQUE_BUG = {}
INDEX_UNIQUE_BUG_IP = {}
INDEX_UNIQUE_BUG_TRACE = {}
INDEX_UNIQUE_BUG_TRACE3 = {}

EXECUTOR = {}

FUZZER_BITMAP = {}

logID = 0
LAST = None

bug_id: Dict[Fuzzer, Dict[str, int]] = {}
bug_id_ip: Dict[Fuzzer, Dict[str, int]] = {}
bug_id_trace: Dict[Fuzzer, Dict[str, int]] = {}
bug_id_trace3: Dict[Fuzzer, Dict[str, int]] = {}

crash_set: Dict[Fuzzer, Set] = {}
crash_set_ip: Dict[Fuzzer, Set] = {}
crash_set_trace: Dict[Fuzzer, Set] = {}
crash_set_trace3: Dict[Fuzzer, Set] = {}

hashmap: Dict[str, str] = dict()

logger = logging.getLogger('autofz.evaluator')


def json_dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


class AFLBitmap:
    BITMAP_SIZE = 1048576

    def __init__(self, bitmap=None):
        self.bitmap = np.array(bytearray())
        if bitmap is not None:
            if isinstance(bitmap, np.ndarray):
                # bitmap is already a converted np.array, leave it as it is
                assert (np.sum(np.where(bitmap > 1, 1, 0)) == 0
                        )  # check if it looks like a converted array
                self.bitmap = np.array(bitmap, copy=True)
            else:
                # bitmap was delivered as an actual AFL bitmap, convert to np.array
                self.bitmap = np.array(bytearray(bitmap), dtype='uint8')
                self.normalize_bitmap()

    @classmethod
    def empty(cls):
        b = bytearray([0]) * cls.BITMAP_SIZE
        bitmap = np.array(b)
        del b
        return cls(bitmap=bitmap)

    def normalize_bitmap(self):
        # it could be an AFL virgin_bits or an AFL trace_bits
        # virgin_bits uses 0xff to say "this edge was not touched"
        # trace_bits uses 0x00 to say the same
        # so only count an edge as visited if it's neither 0xff nor 0x00
        # more reliant than trying to detect if it's coming from virgin_bits or trace_bits

        # NOTE: virgin_bits here
        self.bitmap = np.array(np.where((self.bitmap != 0xff), 1, 0),
                               dtype='uint8')

    def is_new(self, data):
        if len(self.bitmap) == 0:
            return True
        else:
            return data.delta(self.bitmap) > 0

    def initialize_bitmap_if_necessary(self, size):
        if len(self.bitmap) == 0 and size > 0:
            b = bytearray([0]) * size
            self.bitmap = np.array(b)
            del b

    # counts visited edges in bitmap
    def count(self):
        return np.sum(self.bitmap)

    # use other bitmap as baseline, what are the new branches in our bitmap?
    def delta(self, other):
        if len(other.bitmap) > 0:
            self.initialize_bitmap_if_necessary(len(other.bitmap))
        elif len(self.bitmap) > 0:
            other.initialize_bitmap_if_necessary(len(self.bitmap))
        assert (len(self.bitmap) == len(other.bitmap))
        delta = (self.bitmap | other.bitmap) - other.bitmap
        return AFLBitmap(delta)

    def reset(self):
        self.bitmap = np.array(bytearray())

    # use other bitmap as baseline,, how many new branches are in our bitmap?
    def delta_count(self, other):
        return np.sum(self.delta(other).bitmap)

    # update bitmap
    def update(self, other):
        if len(other.bitmap) == 0:
            return
        self.initialize_bitmap_if_necessary(len(other.bitmap))
        assert (len(self.bitmap) == len(other.bitmap))
        u = self.bitmap | other.bitmap
        self.bitmap = u

    def union(self, other):
        if len(other.bitmap) == 0:
            return
        self.initialize_bitmap_if_necessary(len(other.bitmap))
        assert (len(self.bitmap) == len(other.bitmap))
        u = self.bitmap | other.bitmap
        return AFLBitmap(u)

    def __or__(self, other):
        return self.union(other)

    def __add__(self, other):
        return self.union(other)

    def __repr__(self):
        return str(self.bitmap)


class AFLForkserverExecuter(object):
    def __init__(self, binary, arguments):
        script_path = os.path.dirname(os.path.realpath(__file__))

        # if not check_afl():
        #     raise Exception(
        #         "AFL is not configured, please execute:\n"
        #         "sudo bash -c 'echo core >/proc/sys/kernel/core_pattern; cd /sys/devices/system/cpu; echo performance | tee cpu*/cpufreq/scaling_governor'"
        #     )

        self.fuzzed_binary = binary
        self.binary = self.fuzzed_binary
        self.arguments = arguments

        self.script_path = os.path.abspath(
            os.path.dirname(os.path.realpath(__file__)))

        self.input_file_path = None
        while self.input_file_path == None or os.path.isfile(
                self.input_file_path):
            self.randID = random.randint(1111111111, 9999999999)
            self.input_file_path = "/dev/shm/quickcov_input_%d" % (self.randID)
        assert self.input_file_path

        if '@@' in self.arguments:
            self.arguments[self.arguments.index('@@')] = self.input_file_path
        self.arguments.insert(0, os.path.abspath(self.binary))
        # in QEMU mode, we need to do some special stuff
        self.coverage = AFLBitmap()

        # https://github.com/albertz/playground/blob/master/shared_mem.py
        self.aflforkserverlib = ctypes.cdll.LoadLibrary(
            os.path.abspath(os.path.join(self.script_path,
                                         "aflforkserver.so")))

        LP_c_char = ctypes.POINTER(ctypes.c_char)
        LP_LP_c_char = ctypes.POINTER(LP_c_char)

        # int shmget(key_t key, size_t size, int shmflg);

        # void setup(char* out_file_path)
        self.setup = self.aflforkserverlib.setup
        self.setup.restype = None
        self.setup.argtypes = (ctypes.c_char_p, ctypes.c_int)

        # void init_target(char *argv[], char* target)
        self.init_target = self.aflforkserverlib.init_target
        self.init_target.restype = ctypes.c_int
        self.init_target.argtypes = (ctypes.POINTER(ctypes.c_char_p),
                                     ctypes.POINTER(ctypes.c_char))

        # int run_target(char **argv)
        # returns non-zero if error happened
        self.run_target = self.aflforkserverlib.run_target
        self.run_target.restype = ctypes.c_int
        self.run_target.argtypes = (ctypes.POINTER(ctypes.c_char_p), )

        # int check_new_coverage()
        self.check_new_coverage = self.aflforkserverlib.check_new_coverage
        self.check_new_coverage.restype = ctypes.c_int
        self.check_new_coverage.argtypes = None

        # static void write_to_testcase(void* mem, u32 len)
        self.write_to_testcase = self.aflforkserverlib.write_to_testcase
        self.write_to_testcase.restype = None
        self.write_to_testcase.argtypes = (ctypes.POINTER(ctypes.c_char),
                                           ctypes.c_int)

        # int get_map_size()
        self.get_map_size = self.aflforkserverlib.get_map_size
        self.get_map_size.restype = ctypes.c_int
        self.get_map_size.argtypes: Any = None
        self.MAP_SIZE = self.get_map_size()

        # uint8_t* get_bitmap()
        self._get_bitmap = self.aflforkserverlib.get_bitmap
        self._get_bitmap.restype = ctypes.POINTER(ctypes.c_uint8 *
                                                  self.MAP_SIZE)
        self._get_bitmap.argtypes = None

        # int has_exec_failed()
        self.has_exec_failed = self.aflforkserverlib.has_exec_failed
        self.has_exec_failed.restype = ctypes.c_int
        self.has_exec_failed.argtypes = None

        # int cleanup()
        self.afl_cleanup = self.aflforkserverlib.cleanup
        self.afl_cleanup.restype = None
        self.afl_cleanup.argtypes = None

        # void reset_bitmap()
        self._reset = self.aflforkserverlib.reset_bitmap
        self._reset.restype = None
        self._reset.argtypes = None

        # set up aflforkserver
        #(ctypes.c_char * len(self.input_file_path.encode('ascii')))(*self.input_file_path.encode('ascii'))
        # normally .cur_input
        self.input_file_path_c = (self.input_file_path +
                                  "\x00").encode('ascii')
        self.setup(self.input_file_path_c, int(False))
        execve_arguments = [s.encode('ascii') for s in self.arguments] + [
            None
        ]  # execve needs this format [param1, param2, NULL]
        self.arguments_c = (ctypes.c_char_p *
                            len(execve_arguments))(*execve_arguments)
        binary = (self.binary + "\x00").encode(
            'ascii'
        )  # I'm sure there is some ctypes-proper way to do this ... @TODO
        self.binary_c = (ctypes.c_char * len(binary))(*binary)
        exec_failed = self.init_target(self.arguments_c, self.binary_c)
        if exec_failed > 0:
            print("forkserver error")
            raise Exception("AFL Forkserver error")

        self.has_get_coverage = True
        self.new_input = False

    def execute(self, f):
        assert self.input_file_path
        copy2(f, self.input_file_path)
        hasCrashed = False
        hasExited = False
        hasCrashed = (self.run_target(self.arguments_c) == 2)
        self.new_input = (self.check_new_coverage() > 0)
        return hasCrashed

    def get_coverage(self):
        cov = None
        cov = AFLBitmap(self._get_bitmap().contents)
        self.coverage.update(cov)
        return self.coverage

    def get_bitmap(self):
        cov = AFLBitmap(self._get_bitmap().contents)
        return cov

    def reset(self):
        self._reset()
        self.coverage.reset()

    def cleanup(self):
        try:
            assert self.input_file_path
            os.remove(self.input_file_path)
        except:
            pass
        # self.afl_cleanup()
        self.coverage.reset()

    def __del__(self):
        self.cleanup()


class AFLForkserverTask(Enum):
    SET_CORE = 1
    EXECUTE = 2
    GET_COVERAGE = 3
    RESET = 4
    CLEANUP = 5
    GET_BITMAP = 6


class AFLForkserverProcess(object):
    def __init__(self, binary, binary_arguments):
        self.binary = binary
        self.binary_arguments = binary_arguments
        self.running = True
        self.queue = Queue()
        self.parent, self.child = Pipe()
        self.p = Process(target=self.process_loop, daemon=True)
        self.p.start()

    def process_loop(self):
        self.afl = AFLForkserverExecuter(self.binary, self.binary_arguments)
        while self.running:
            if self.child.poll(timeout=1):
                (task, args) = self.child.recv()
            else:
                continue

            if task == AFLForkserverTask.EXECUTE:
                self.child.send(self.afl.execute(*args))
            elif task == AFLForkserverTask.GET_COVERAGE:
                self.child.send(self.afl.get_coverage(*args))
            elif task == AFLForkserverTask.GET_BITMAP:
                self.child.send(self.afl.get_bitmap(*args))
            elif task == AFLForkserverTask.RESET:
                self.child.send(self.afl.reset())
            elif task == AFLForkserverTask.SET_CORE:
                assert (args[0] < os.cpu_count())
                os.system("taskset -p -c %d %d" % (args[0], self.p.pid))
            elif task == AFLForkserverTask.CLEANUP:
                ret = self.afl.cleanup()
                self.running = False
                self.child.send(ret)
                self.child.close()
            else:
                assert (False)  # should never reach this

    def execute(self, f):
        self.parent.send((AFLForkserverTask.EXECUTE, [f]))
        return self._parent_recv()

    def get_coverage(self):
        self.parent.send((AFLForkserverTask.GET_COVERAGE, []))
        return self._parent_recv()

    def get_bitmap(self):
        self.parent.send((AFLForkserverTask.GET_BITMAP, []))
        return self._parent_recv()

    def reset(self):
        self.parent.send((AFLForkserverTask.RESET, []))
        return self._parent_recv()

    def set_core(self, core):
        self.parent.send((AFLForkserverTask.SET_CORE, [core]))

    def cleanup(self):
        try:
            self.parent.send((AFLForkserverTask.CLEANUP, []))
            self._parent_recv()
            self.parent.close()
        except (EOFError, OSError):
            pass
        return

    def restart_forkserver(self):
        self.running = False
        self.p = Process(target=self.process_loop, daemon=True)
        self.p.start()

    # recv with timeout
    def _parent_recv(self):
        if self.parent.poll(timeout=1000):
            return self.parent.recv()
        else:
            print('restart Forkserver because of timeout')
            self.restart_forkserver()
            raise Exception("Forserver poll timeout")

    def __del__(self):
        self.cleanup()

    def stop(self):
        self.p.kill()


def get_all_names(include_global=True):
    global FUZZERS
    ret = FUZZERS
    if include_global:
        return ret + ['global']
    return ret


def get_eval_fuzzer_root(fuzzer: str) -> Optional[Path]:
    global ARGS, FUZZERS
    if fuzzer in FUZZERS or fuzzer == 'global':
        return ARGS.output / 'eval' / fuzzer
    else:
        raise ValueError


def get_fuzzer_root(fuzzer: str) -> Optional[Path]:
    global ARGS, FUZZERS
    if fuzzer in FUZZERS:
        return ARGS.output / ARGS.target / fuzzer
    elif fuzzer == 'global':
        return ARGS.output / ARGS.target
    else:
        raise ValueError


def init():
    global MAP, INDEX, EXECUTOR, FUZZER_BITMAP
    global bug_id, bug_id_ip, bug_id_trace, bug_id_trace3
    MAP['dirs'] = {}
    MAP['top_dir'] = top_dir = ARGS.output / 'eval'
    MAP['debug_file'] = top_dir / 'debug.log'
    MAP['profile_file'] = top_dir / 'profile.log'
    MAP['log_file'] = top_dir / 'eval.log'
    MAP['log_file_latest'] = top_dir / 'eval-latest.log'
    MAP['seed_finished_file'] = top_dir / 'seed-finished'
    MAP['lock_path'] = top_dir / 'lock'
    MAP['coverage_path'] = top_dir / 'cov.json'
    os.makedirs(top_dir, exist_ok=True)

    binary, binary_arguments = find_executable_from_cmd()
    for fuzzer in get_all_names():
        eval_fuzzer_root = get_eval_fuzzer_root(fuzzer)
        assert eval_fuzzer_root
        dir_crashes = eval_fuzzer_root / 'crashes'
        dir_unique_bugs = eval_fuzzer_root / 'unique_bugs'
        dir_unique_bugs_ip = eval_fuzzer_root / 'unique_bugs_ip'
        dir_unique_bugs_trace = eval_fuzzer_root / 'unique_bugs_trace'
        dir_unique_bugs_trace3 = eval_fuzzer_root / 'unique_bugs_trace3'
        os.makedirs(eval_fuzzer_root, exist_ok=True)
        os.makedirs(dir_crashes, exist_ok=True)
        os.makedirs(dir_unique_bugs, exist_ok=True)
        os.makedirs(dir_unique_bugs_ip, exist_ok=True)
        os.makedirs(dir_unique_bugs_trace, exist_ok=True)
        os.makedirs(dir_unique_bugs_trace3, exist_ok=True)
        FUZZER_BITMAP[fuzzer] = AFLBitmap.empty()
        EXECUTOR[fuzzer] = AFLForkserverProcess(binary, binary_arguments)
        PROCESSED_FILE[fuzzer] = set()
        PROCESSED_CHECKSUM[fuzzer] = set()
        crash_set[fuzzer] = set()
        crash_set_ip[fuzzer] = set()
        crash_set_trace[fuzzer] = set()
        crash_set_trace3[fuzzer] = set()
        bug_id[fuzzer] = dict()
        bug_id_ip[fuzzer] = dict()
        bug_id_trace[fuzzer] = dict()
        bug_id_trace3[fuzzer] = dict()
        INDEX[fuzzer] = 0
        INDEX_UNIQUE_BUG[fuzzer] = 0
        INDEX_UNIQUE_BUG_IP[fuzzer] = 0
        INDEX_UNIQUE_BUG_TRACE[fuzzer] = 0
        INDEX_UNIQUE_BUG_TRACE3[fuzzer] = 0


def log(msg):
    global MAP
    with open(MAP['log_file'], 'a') as f:
        f.write(f'{msg}\n')


def log_latest(msg, append=False):
    global MAP
    mode = 'a' if append else 'w'
    with open(MAP['log_file_latest'], mode) as f:
        f.write(f'{msg}\n')


def log_debug(msg):
    global MAP
    with open(MAP['debug_file'], 'a') as f:
        f.write(f'{msg}\n')


def log_profile(msg):
    global MAP
    with open(MAP['profile_file'], 'a') as f:
        f.write(f'{msg}\n')


def debug(*args, **kwargs):
    if not IS_DEBUG: return
    log(*args, **kwargs)


def gen_id(fuzzer):
    global INDEX
    ret = INDEX[fuzzer]
    INDEX[fuzzer] += 1
    return ret


def gen_unique_bug_id(fuzzer):
    global INDEX_UNIQUE_BUG
    ret = INDEX_UNIQUE_BUG[fuzzer]
    INDEX_UNIQUE_BUG[fuzzer] += 1
    return ret


def gen_unique_bug_id_ip(fuzzer):
    global INDEX_UNIQUE_BUG_IP
    ret = INDEX_UNIQUE_BUG_IP[fuzzer]
    INDEX_UNIQUE_BUG_IP[fuzzer] += 1
    return ret


def gen_unique_bug_id_trace(fuzzer):
    global INDEX_UNIQUE_BUG_TRACE
    ret = INDEX_UNIQUE_BUG_TRACE[fuzzer]
    INDEX_UNIQUE_BUG_TRACE[fuzzer] += 1
    return ret


def gen_unique_bug_id_trace3(fuzzer):
    global INDEX_UNIQUE_BUG_TRACE3
    ret = INDEX_UNIQUE_BUG_TRACE3[fuzzer]
    INDEX_UNIQUE_BUG_TRACE3[fuzzer] += 1
    return ret


def get_crash_dirs(fuzzer):
    def_dir = get_fuzzer_root(fuzzer)
    assert def_dir
    crash_dir_pattern = ARGS.crash_case_dir
    ret = []
    for crash_dir in pathlib.Path(def_dir).rglob(f'**/{crash_dir_pattern}'):
        crash_dir = str(crash_dir)
        if 'crashrunner' in crash_dir: continue
        ret.append(crash_dir)
    return ret


def get_queue_dirs(fuzzer, pattern='queue'):
    def_dir = get_fuzzer_root(fuzzer)
    assert def_dir
    queue_dir_pattern = pattern
    ret = []
    for queue_dir in pathlib.Path(def_dir).rglob(f'**/{queue_dir_pattern}'):
        queue_dir = str(queue_dir)
        if utils.is_dir(queue_dir):
            ret.append(queue_dir)
    return ret


def get_fuzzers():
    global ARGS
    target_dir = os.path.join(ARGS.output, ARGS.target)
    ret = []
    for fuzzer in pathlib.Path(target_dir).glob(f'*'):
        fuzzer = str(fuzzer)
        if utils.is_dir(fuzzer):
            ret.append(os.path.basename(fuzzer))
    return ret


def import_dir_files(cdir, pattern='*'):
    path = os.path.join(cdir, pattern)
    return sorted(glob.glob(path))


def run_cmd(cmd, out_path, err_path, env=None):

    fout = open(out_path, 'w')
    ferr = open(err_path, 'w')

    cmd = cmd
    if ARGS.timeout:
        cmd = f'timeout --preserve-status -s INT {ARGS.timeout} {cmd}'
    if env:
        envs = utils.to_env_string(env)
        cmd = f'{envs} {cmd}'
    sp = subprocess.call(cmd,
                         shell=True,
                         stdin=subprocess.DEVNULL,
                         stdout=fout,
                         stderr=ferr)

    fout.close()
    ferr.close()


def gen_crash_cmd():
    return f'{ARGS.binary_crash} {ARGS.args}'


def symlink(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    os.symlink(src, dst)


def symlink2(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    rel_path = os.path.relpath(src, os.path.dirname(dst))
    os.symlink(rel_path, dst)


def run_crash(crash, directory, copy_before_run=True):
    global MAP
    cmd = gen_crash_cmd()
    env = {'ASAN_OPTIONS': ASAN_OPTIONS}
    crash = os.path.realpath(crash)
    out_path = os.path.join(directory, 'out')
    err_path = os.path.join(directory, 'err')
    fin = os.path.join(directory, 'input')
    rel_path = os.path.relpath(crash, os.path.dirname(fin))
    symlink(rel_path, fin)

    input_file = crash
    if copy_before_run:
        cur_input_name = os.path.join(MAP['top_dir'], '.cur_input')
        copy2(crash, cur_input_name)
        input_file = cur_input_name

    cmd = cmd.replace('@@', input_file)
    run_cmd(cmd=cmd, out_path=out_path, err_path=err_path, env=env)


def parse_asan(ferr):
    result = {}
    result['trace'] = []
    with open(ferr, 'r', encoding="latin-1", errors='ignore') as f:
        for line in f:
            if line.startswith('####'):
                parsed = line.split('####')
                ip = parsed[1]
                func = parsed[2]
                source = parsed[3]
                frame = parsed[4]
                result['trace'].append((ip, func, source, frame))
            if 'AddressSanitizer' in line:
                result['interesting'] = line
    debug(f'parse_asan result is {result}')
    return result


def hash_trace(asan_trace):
    ret = None
    sha256 = hashlib.sha256()
    for trace in asan_trace:
        ip, func, source, frame = trace
        sha256.update(func.encode())
    ret = sha256.hexdigest()
    return ret


def hash_trace3(asan_trace):
    '''
    only top 3 frame
    '''
    ret = None
    sha256 = hashlib.sha256()
    asan_trace = asan_trace[0:3]
    for trace in asan_trace:
        ip, func, source, frame = trace
        sha256.update(func.encode())
    ret = sha256.hexdigest()
    return ret


def hash_ip(asan_trace):
    ret = None
    sha256 = hashlib.sha256()
    # NOTE: empty will only has an unique hash
    if len(asan_trace):
        last = asan_trace[0]
        ip, func, source, frame = last
        sha256.update(ip.encode())
    ret = sha256.hexdigest()
    return ret


BUF_SIZE = 65536


def checksum(filename):
    assert os.path.isabs(filename)
    if filename in hashmap:
        return hashmap[filename]
    t = time.time()
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    ret = md5.hexdigest()
    hashmap[filename] = ret
    return ret


PROCESSED_FILE: Dict[Fuzzer, Set] = {}
PROCESSED_CHECKSUM: Dict[Fuzzer, Set] = {}

PROCESSED_LOCK = threading.Lock()


def add_processed(fuzzer, filename):
    global PROCESSED_CHECKSUM, PROCESSED_FILE
    assert os.path.isabs(filename)
    c = checksum(filename)
    with PROCESSED_LOCK:
        PROCESSED_FILE[fuzzer].add(filename)
        PROCESSED_CHECKSUM[fuzzer].add(c)
        PROCESSED_FILE['global'].add(filename)
        PROCESSED_CHECKSUM['global'].add(c)


def is_processed(fuzzer, filename):
    global PROCESSED_CHECKSUM, PROCESSED_FILE
    assert os.path.isabs(filename)
    if filename in PROCESSED_FILE[fuzzer]:
        return True
    c = checksum(filename)
    return c in PROCESSED_CHECKSUM[fuzzer]


def find_executable_from_cmd():
    global ARGS
    binary = ARGS.binary
    binary_arguments = ARGS.args.split(' ')
    return binary, binary_arguments


BLACKLIST = [
    'README.txt',  # afl
]


def in_blacklist(f):
    global BLACKLIST
    basename = os.path.basename(f)
    for bl in BLACKLIST:
        if bl in basename: return True
    return False


def save_fuzzer_bitmap(fuzzer):
    eval_fuzzer_root = get_eval_fuzzer_root(fuzzer)
    assert eval_fuzzer_root
    bitmap_path = eval_fuzzer_root / 'bitmap'
    fuzzer_bitmap = FUZZER_BITMAP[fuzzer].bitmap
    lock_path = MAP['lock_path']
    lock = filelock.FileLock(lock_path, timeout=100)
    with lock:
        with open(bitmap_path, 'wb+') as f:
            f.write(fuzzer_bitmap)


def save_fuzzer_crashes(fuzzer):
    eval_fuzzer_root = get_eval_fuzzer_root(fuzzer)
    assert eval_fuzzer_root
    log_path = eval_fuzzer_root / 'crashrunner-latest.log'
    log_path_new = eval_fuzzer_root / 'crashrunner-new-latest.json'
    lock_path = MAP['lock_path']
    lock = filelock.FileLock(lock_path, timeout=100)
    m = {}
    m['unique_bugs'] = len(crash_set[fuzzer])
    m['unique_bugs_ip'] = len(crash_set_ip[fuzzer])
    m['unique_bugs_trace'] = len(crash_set_trace[fuzzer])
    m['unique_bugs_trace3'] = len(crash_set_trace3[fuzzer])

    with lock:
        with open(log_path, 'w') as f:
            msg = f'unique bugs: {len(crash_set[fuzzer])}\n'
            f.write(msg)

        with open(log_path_new, 'w') as f:
            msg = json.dumps(m, default=json_dumper)
            f.write(f'{msg}')


def add_all_bitmap():
    global EXECUTOR
    for fuzzer in get_all_names(False):
        afl_bitmap_f = EXECUTOR[fuzzer].get_bitmap()
        add_fuzzer_bitmap(fuzzer, afl_bitmap_f)


def save_all_bitmap(add=True):
    if add:
        add_all_bitmap()
    for fuzzer in get_all_names():
        save_fuzzer_bitmap(fuzzer)


def save_all_crash(add=True):
    for fuzzer in get_all_names():
        save_fuzzer_crashes(fuzzer)


BITMAP_LOCK = threading.Lock()


def add_fuzzer_bitmap(fuzzer, bitmap):
    global FUZZER_BITMAP, BITMAP_LOCK
    with BITMAP_LOCK:
        FUZZER_BITMAP[fuzzer] |= bitmap
        FUZZER_BITMAP['global'] |= bitmap


def sync():
    global BITMAP_LOCK, FUZZER_BITMAP, PROCESSED_CHECKSUM
    global PROCESSED_FILE
    global PROCESSED_LOCK
    start = time.time()
    with BITMAP_LOCK:
        with PROCESSED_LOCK:
            for fuzzer in get_all_names(False):
                FUZZER_BITMAP['global'] |= FUZZER_BITMAP[fuzzer]
            log_profile(f'phase1: {time.time()-start}s')
            for fuzzer in get_all_names():
                start2 = time.time()
                FUZZER_BITMAP[fuzzer] = copy.deepcopy(FUZZER_BITMAP['global'])
                PROCESSED_CHECKSUM[fuzzer] = copy.copy(
                    PROCESSED_CHECKSUM['global'])
                PROCESSED_FILE[fuzzer] = copy.copy(PROCESSED_FILE['global'])
                log_profile(
                    f'phase2: {fuzzer} {time.time()-start2}s, {time.time()-start}s'
                )
                save_fuzzer_bitmap(fuzzer)
        log_profile(f'overall: {time.time()-start}s')


def process_fuzzer_queue_one(fuzzer, f):
    global MAP, ARGS, EXECUTOR
    if in_blacklist(f): return
    if not os.path.isfile(f): return
    is_p = is_processed(fuzzer, f)
    checksum_f = checksum(f)
    afl_bitmap_f = None
    if not is_p:
        EXECUTOR[fuzzer].execute(f)
    add_processed(fuzzer, f)


def process_crash_one(fuzzer, f):
    global MAP, ARGS
    if in_blacklist(f): return
    if not os.path.isfile(f): return
    is_p = is_processed(fuzzer, f)
    if is_p: return
    add_processed(fuzzer, f)
    eval_fuzzer_root = get_eval_fuzzer_root(fuzzer)
    assert eval_fuzzer_root
    dir_crashes = eval_fuzzer_root / 'crashes'
    dir_unique_bugs = eval_fuzzer_root / 'unique_bugs'
    dir_unique_bugs_ip = eval_fuzzer_root / 'unique_bugs_ip'
    dir_unique_bugs_trace = eval_fuzzer_root / 'unique_bugs_trace'
    dir_unique_bugs_trace3 = eval_fuzzer_root / 'unique_bugs_trace3'
    new_id = gen_id(fuzzer)
    new_dir = dir_crashes / str(new_id)
    os.makedirs(new_dir, exist_ok=True)
    run_crash(crash=f, directory=new_dir, copy_before_run=True)
    out_path = new_dir / 'out'
    err_path = new_dir / 'err'
    debug(err_path)
    asan_output = parse_asan(err_path)

    ID = None
    ID_trace = trace_hash = hash_trace(asan_output['trace'])
    ID_trace3 = trace3_hash = hash_trace3(asan_output['trace'])
    ID_ip = ip_hash = hash_ip(asan_output['trace'])

    crash_set_trace[fuzzer].add(trace_hash)
    crash_set_trace3[fuzzer].add(trace3_hash)
    crash_set_ip[fuzzer].add(ip_hash)

    if ARGS.mode == 'trace':
        ID = trace_hash
    elif ARGS.mode == 'trace3':
        ID = trace3_hash
    elif ARGS.mode == 'ip':
        ID = ip_hash

    assert ID
    crash_set[fuzzer].add(ID)

    if ID not in bug_id[fuzzer]:
        bug_id[fuzzer][ID] = gen_unique_bug_id(fuzzer)

    if ID_ip not in bug_id_ip[fuzzer]:
        bug_id_ip[fuzzer][ID_ip] = gen_unique_bug_id_ip(fuzzer)

    if ID_trace not in bug_id_trace[fuzzer]:
        bug_id_trace[fuzzer][ID_trace] = gen_unique_bug_id_trace(fuzzer)

    if ID_trace3 not in bug_id_trace3[fuzzer]:
        bug_id_trace3[fuzzer][ID_trace3] = gen_unique_bug_id_trace3(fuzzer)

    new_unique_bug_dir = dir_unique_bugs / str(bug_id[fuzzer][ID])
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)

    new_unique_bug_dir = dir_unique_bugs_ip / str(bug_id_ip[fuzzer][ID_ip])
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)

    new_unique_bug_dir = dir_unique_bugs_trace / str(
        bug_id_trace[fuzzer][ID_trace])
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)

    new_unique_bug_dir = os.path.join(dir_unique_bugs_trace3,
                                      str(bug_id_trace3[fuzzer][ID_trace3]))
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)

    # add to global
    eval_fuzzer_root = get_eval_fuzzer_root('global')
    assert eval_fuzzer_root
    dir_unique_bugs = eval_fuzzer_root / 'unique_bugs'
    dir_unique_bugs_ip = eval_fuzzer_root / 'unique_bugs_ip'
    dir_unique_bugs_trace = eval_fuzzer_root / 'unique_bugs_trace'
    dir_unique_bugs_trace3 = eval_fuzzer_root / 'unique_bugs_trace3'
    crash_set['global'].add(ID)
    crash_set_ip['global'].add(ID_ip)
    crash_set_trace['global'].add(ID_trace)
    crash_set_trace3['global'].add(ID_trace3)

    if ID not in bug_id['global']:
        bug_id['global'][ID] = gen_unique_bug_id('global')

    if ID_ip not in bug_id_ip['global']:
        bug_id_ip['global'][ID_ip] = gen_unique_bug_id_ip('global')

    if ID_trace not in bug_id_trace['global']:
        bug_id_trace['global'][ID_trace] = gen_unique_bug_id_trace('global')

    if ID_trace3 not in bug_id_trace3['global']:
        bug_id_trace3['global'][ID_trace3] = gen_unique_bug_id_trace3('global')

    new_unique_bug_dir = dir_unique_bugs / str(bug_id['global'][ID])
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)

    new_unique_bug_dir = dir_unique_bugs_ip / str(bug_id_ip['global'][ID_ip])
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)

    new_unique_bug_dir = dir_unique_bugs_trace / str(
        bug_id_trace['global'][ID_trace])
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)

    new_unique_bug_dir = dir_unique_bugs_trace3 / str(
        bug_id_trace3['global'][ID_trace3])
    os.makedirs(new_unique_bug_dir, exist_ok=True)
    rel_path = os.path.relpath(new_dir, new_unique_bug_dir)
    dest = os.path.join(new_unique_bug_dir, os.path.basename(new_dir))
    symlink(rel_path, dest)
    # log(f'{err_path}, {ID}, {bug_id[ID]}, {len(crash_set)}')


def process_coverage_fuzzer_files(fuzzer_files):
    THRESHOLD = 1000
    counter = 0
    l = len(fuzzer_files)
    for fuzzer, f in fuzzer_files:
        process_fuzzer_queue_one(fuzzer, f)
        counter += 1
        if counter % THRESHOLD == 0:
            logger.debug(f'process coverage files count : {counter}/{l}')
            save_all_bitmap(True)
    save_all_bitmap(True)


def process_crash_fuzzer_files(fuzzer_files):
    for fuzzer, f in fuzzer_files:
        process_crash_one(fuzzer, f)
        # process_crash_one('global', f)


def get_coverage_fuzzer_files(fuzzer):
    global PROCESSED_FILE, ARGS
    queue_dirs = get_queue_dirs(fuzzer)
    # seed dir
    queue_dirs.append(ARGS.input)
    total = 0
    ret = []
    for queue_dir in queue_dirs:
        files = import_dir_files(queue_dir)
        for f in files:
            if f in PROCESSED_FILE[fuzzer]: continue
            ret.append((fuzzer, f))
    return ret


def get_crash_fuzzer_files(fuzzer):
    global PROCESSED_FILE
    crash_dirs = get_crash_dirs(fuzzer)
    total = 0
    ret = []
    for crash_dir in crash_dirs:
        files = import_dir_files(crash_dir)
        for f in files:
            if f in PROCESSED_FILE[fuzzer]: continue
            ret.append((fuzzer, f))
    return ret


FIRST_COVERAGE = True
FIRST_CRASH = True


def process_coverage():
    global ARGS, MAP, FIRST_COVERAGE
    while True:
        fuzzer_files = []
        for fuzzer in get_all_names(False):
            fuzzer_files += get_coverage_fuzzer_files(fuzzer)
        if fuzzer_files:
            # to keep fair
            random.shuffle(fuzzer_files)
            process_coverage_fuzzer_files(fuzzer_files)
            save_all_bitmap()
            FIRST_COVERAGE = False
        else:
            log('coverage: no new files')
        if FIRST_COVERAGE:
            save_all_bitmap()
            FIRST_COVERAGE = False
        if not ARGS.live:
            return
        time.sleep(ARGS.sleep)


def process_crash():
    global ARGS, MAP, FIRST_CRASH
    while True:
        fuzzer_files = []
        for fuzzer in get_all_names(False):
            fuzzer_files += get_crash_fuzzer_files(fuzzer)
        if fuzzer_files:
            process_crash_fuzzer_files(fuzzer_files)
            save_all_crash()
            FIRST_CRASH = False
        else:
            log('crash: no new files')
        if FIRST_COVERAGE:
            save_all_crash()
        if not ARGS.live:
            return
        time.sleep(ARGS.sleep)


def coverage_thread():
    process_coverage()


def crash_thread():
    process_crash()


def get_fuzzer_files(fuzzer: Fuzzer) -> Tuple[List[Path], List[Path]]:
    global ARGS
    coverage_files = []
    crash_files = []
    fuzzer_root_dir = get_fuzzer_root(fuzzer)
    assert fuzzer_root_dir
    if not fuzzer_root_dir.exists():
        return [], []
    assert fuzzer_root_dir
    if utils.fuzzer_has_subdir(FuzzerType(fuzzer)):
        for subdir in fuzzer_root_dir.iterdir():
            if subdir.is_dir():
                if subdir.parts[-1] == 'autofz': continue
                watcher.init_watcher(fuzzer, subdir)
    else:
        watcher.init_watcher(fuzzer, fuzzer_root_dir)
    # not ready
    if fuzzer not in watcher.WATCHERS:
        return [], []
    watchers = watcher.WATCHERS[fuzzer]
    for w in watchers:
        # prevent iterating while changing
        last_index = LAST_INDEX.get(w, -1)
        queue_len = len(w.test_case_queue)
        for i in range(last_index + 1, queue_len):
            test_case_path = w.test_case_queue[i]
            if w._ignore_test_case(test_case_path):
                continue
            seed_type = w._get_test_case_type(test_case_path)
            if seed_type == SeedType.NORMAL or seed_type == SeedType.HANG:
                coverage_files.append(test_case_path)
            elif seed_type == SeedType.CRASH:
                crash_files.append(test_case_path)
            else:
                assert False, 'unknow seed type'
        LAST_INDEX[w] = queue_len

    return coverage_files, crash_files


def save_coverage():
    global MAP
    ret = {}
    ret['coverage'] = {}
    ret['unique_bugs'] = {}
    ret['unique_bugs_ip'] = {}
    ret['unique_bugs_trace'] = {}
    ret['unique_bugs_trace3'] = {}
    for fuzzer in get_all_names():
        ret['coverage'][fuzzer] = int(FUZZER_BITMAP[fuzzer].count())
        ret['unique_bugs'][fuzzer] = len(crash_set[fuzzer])
        ret['unique_bugs_ip'][fuzzer] = len(crash_set_ip[fuzzer])
        ret['unique_bugs_trace'][fuzzer] = len(crash_set_trace[fuzzer])
        ret['unique_bugs_trace3'][fuzzer] = len(crash_set_trace3[fuzzer])
    with open(MAP['coverage_path'], 'w') as f:
        f.write(json.dumps(ret, default=json_dumper))


def watcher_thread():
    while True:
        all_coverage_files = []
        all_crash_files = []

        for fuzzer in get_all_names(False):
            coverage_files, crash_files = get_fuzzer_files(fuzzer)
            for f in coverage_files:
                all_coverage_files.append((fuzzer, f))
            for f in crash_files:
                all_crash_files.append((fuzzer, f))

        if all_coverage_files:
            process_coverage_fuzzer_files(all_coverage_files)
        else:
            log('coverage: no new files')
        if all_crash_files:
            process_crash_fuzzer_files(all_crash_files)
            log('crash: no new files')
        save_all_bitmap()
        save_all_crash()
        save_coverage()

        if not ARGS.live:
            return

        time.sleep(ARGS.sleep)


def handler(signal, frame):
    print('CTRL-C pressed!')
    for fuzzer in get_all_names():
        EXECUTOR[fuzzer].stop()
    sys.exit(0)


def parse_args_fuzzers(args_fuzzers):
    ret = []
    for args_fuzzer in args_fuzzers:
        ret += args_fuzzer.split(' ')
    return ret


def main(raw_args=None):
    global ARGS, FUZZERS
    ARGS = ArgsParser().parse_args(raw_args)
    logger.debug(f'evaluator ARGS is {ARGS}')
    if ARGS.fuzzers:
        FUZZERS = parse_args_fuzzers(ARGS.fuzzers)
    else:
        FUZZERS = get_fuzzers()
    init()

    # handle initial seeds
    input_files = import_dir_files(ARGS.input)

    for f in get_all_names(False):
        fuzzer_files = [(f, inf) for inf in input_files]
        process_coverage_fuzzer_files(fuzzer_files)

    save_all_bitmap()
    save_all_crash()
    save_coverage()
    # seed only: used to evaluate coverage post run
    if ARGS.input_only:
        logger.debug(f'Only evaluate seeds')
        pathlib.Path(MAP['seed_finished_file']).touch(mode=0o666,
                                                      exist_ok=True)
        logger.debug(f'Finished evaluating seeds')
        return None

    thread_watcher = threading.Thread(target=watcher_thread, daemon=True)
    thread_watcher.start()
    return thread_watcher


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    sys.exit(main())
