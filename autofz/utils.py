#!/usr/bin/env python3
import datetime
import os
import random
import re
import string
import sys

# FIXME
if __package__ is None:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    __package__ = "autofz"

from .mytype import Fuzzer, FuzzerType

# https://gist.github.com/santiagobasulto/698f0ff660968200f873a2f9d1c4113c
TIMEDELTA_REGEX = (r'((?P<days>-?\d+)d)?'
                   r'((?P<hours>-?\d+)h)?'
                   r'((?P<minutes>-?\d+)m)?'
                   r'((?P<seconds>-?\d+)s)?')
TIMEDELTA_PATTERN = re.compile(TIMEDELTA_REGEX, re.IGNORECASE)


def parse_delta(delta):
    """ Parses a human readable timedelta (3d5h19m) into a datetime.timedelta.
    Delta includes:
    * Xd days
    * Xh hours
    * Xm minutes
    Values can be negative following timedelta's rules. Eg: -5h-30m
    """
    match = TIMEDELTA_PATTERN.match(delta)
    if match:
        parts = {k: int(v) for k, v in match.groupdict().items() if v}
        return datetime.timedelta(**parts)


def time_to_seconds(delta) -> int:
    if type(delta) is int:
        return delta
    if type(delta) is float:
        return int(delta)
    ret = parse_delta(delta)
    assert ret
    return int(ret.total_seconds())


def seconds_to_time(seconds, all_seconds=False):
    if all_seconds:
        return f'{seconds}s'
    hours = int(seconds // 3600)
    seconds -= hours * 3600
    minutes = int(seconds // 60)
    seconds -= minutes * 60
    seconds = int(seconds)

    ret = ''
    if hours: ret += f'{hours}h'
    if minutes: ret += f'{minutes}m'
    if seconds: ret += f'{seconds}s'
    return ret


def time_add(t1, t2, all_seconds=False):
    st1 = time_to_seconds(t1)
    st2 = time_to_seconds(t2)
    return seconds_to_time(st1 + st2, all_seconds)


def quote_command(command):
    return f"bash -c '{command}'"


def to_env_string(env):
    ret = ''
    for k, v in env.items():
        if type(v) == str:
            v.replace('"', '\\"')  # escape
        ret += f'{k}="{v}" '
    return ret


def is_dir(dpath):
    return os.path.exists(dpath) and os.path.isdir(dpath)


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def is_afl_based(fuzzer: Fuzzer) -> bool:
    if (fuzzer == FuzzerType.AFL or fuzzer == FuzzerType.AFLFAST
            or fuzzer == FuzzerType.MOPT or fuzzer == FuzzerType.FAIRFUZZ
            or fuzzer == FuzzerType.LEARNAFL or fuzzer == FuzzerType.RADAMSA
            or fuzzer == FuzzerType.REDQUEEN or fuzzer == FuzzerType.LAFINTEL):
        return True
    return False


def fuzzer_has_subdir(fuzzer: FuzzerType) -> bool:
    if (fuzzer == FuzzerType.AFL or fuzzer == FuzzerType.AFLFAST
            or fuzzer == FuzzerType.MOPT or fuzzer == FuzzerType.FAIRFUZZ
            or fuzzer == FuzzerType.LEARNAFL or fuzzer == FuzzerType.RADAMSA
            or fuzzer == FuzzerType.REDQUEEN or fuzzer == FuzzerType.LAFINTEL
            or fuzzer == FuzzerType.QSYM or fuzzer == FuzzerType.ANGORA):
        return True
    return False


def get_random_string(N):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(N))


def test():
    t1 = '1h'
    t2 = '10m'
    t3 = '60s'
    t4 = '3000s'
    st1 = time_to_seconds(t1)
    st2 = time_to_seconds(t2)
    st3 = time_to_seconds(t3)
    st4 = time_to_seconds(t4)
    assert st1 == 3600
    assert st2 == 600
    assert st3 == 60
    assert st4 == 3000
    _st3 = st1 + st2
    _t3 = seconds_to_time(_st3)
    assert _t3 == '1h10m', _t3
    assert _t3 == time_add(t1, t2)


if __name__ == '__main__':
    test()
