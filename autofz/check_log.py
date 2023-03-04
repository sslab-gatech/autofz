#!/usr/bin/env python3
import os
import argparse
import json
import glob
import logging
import sys

# FIXME
if __package__ is None:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    __package__ = "autofz"

from .common import IS_DEBUG
from . import utils

logger = logging.getLogger('autofz.check_log')


def is_autofz_log(log_file):
    log = None
    try:
        with open(log_file, 'r') as f:
            log = json.load(f)
    except json.decoder.JSONDecodeError:
        logger.error(f'{log_file} json decode error')
        return False
    if 'autofz_args' in log:
        return True
    return False


def get_timeout_from_log(log):
    autofz_args = log['autofz_args']
    autofz_config = log['autofz_config']
    timeout = autofz_args['timeout']
    seconds = utils.parse_delta(timeout).total_seconds()
    return seconds


def check_log_one(log_file, timeout):
    timeout_seconds = utils.parse_delta(timeout).total_seconds()
    log = None
    try:
        with open(log_file, 'r') as f:
            log = json.load(f)
    except json.decoder.JSONDecodeError:
        logger.error(f'{log_file} json decode error')
        return False
    start_time = log['start_time']
    end_time = log.get('end_time', start_time)
    elasp = end_time - start_time
    logger.debug(f'{log_file}: {elasp/3600} hours')
    log_timeout_seconds = get_timeout_from_log(log)
    if log_timeout_seconds < timeout_seconds:
        return False
    if elasp < log_timeout_seconds:
        logger.error(f'{log_file}, {elasp}, {log_timeout_seconds}')
        return False
    else:
        logs = log['log']
        if len(logs) == 0:
            logger.error(f'{log_file} log is empty, must check!!!')
            return False
    return True


def check_log_files(directory, timeout):

    timeout_seconds = utils.parse_delta(timeout).total_seconds()
    log_files = glob.glob(f'{directory}/**/*.json', recursive=True)
    for log_file in log_files:
        is_log = is_autofz_log(log_file)
        logger.debug(f'{log_file}, {is_log}')
        if is_log: check_log_one(log_file, timeout)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-T", dest="timeout", type=str, default='24h')
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--directory')
    group.add_argument("log_file", nargs='?')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(args)
    logger.debug(f'args is {args}')
    if args.directory:
        directory = os.path.realpath(args.directory)
        check_log_files(directory=directory, timeout=args.timeout)
    elif args.log_file:
        if is_autofz_log(args.log_file):
            ret = check_log_one(log_file=args.log_file, timeout=args.timeout)
        else:
            logger.error('{args.log_file} is not autofz\'s log')
            exit(1)
        if ret:
            exit(0)
        else:
            exit(1)
