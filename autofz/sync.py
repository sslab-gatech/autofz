#!/usr/bin/env python3
'''
sync current inputs from one fuzzer to another fuzzer

1. create subdirectory autofz in each fuzzer directory following AFL structure
2. collect inputs from different fuzzers
3. deduplicate
4. copy inputs to directory in first step

'''

import glob
import hashlib
import logging
import os
import pathlib
import time
from pathlib import Path
from typing import Dict, List

from . import config as Config
from . import utils, watcher
from .common import nested_dict
from .mytype import Fuzzer, Fuzzers, FuzzerType

config = Config.CONFIG

logger = logging.getLogger('autofz.sync')

index = nested_dict()

hashmap: Dict[str, str] = dict()
time_for_hash: float = 0


def checksum(filename: str) -> str:
    BUF_SIZE = 65536
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
    global time_for_hash
    time_for_hash += time.time() - t
    ret = md5.hexdigest()
    hashmap[filename] = ret
    return ret


class TestCase(object):
    def __init__(self, filename: Path):
        self.filename = filename
        self.__checksum = None

    @property
    def checksum(self):
        if not self.__checksum:
            self.__checksum = checksum(str(self.filename))
        return self.__checksum


# p2p synced pair, directed, sortd, stored last synced index
# e.g. SYNC_PAIR['afl']['aflfast'] = -1
SYNC_PAIR: Dict[Fuzzer, Dict[Fuzzer, Dict[watcher.Watcher, int]]] = {}

LAST_INDEX: Dict[watcher.Watcher, int] = {}

global_processed_checksum = set()

processed_checksum = nested_dict()


def init_dir(autofz_dir: Path) -> None:
    '''
    create afl-compatible directory structure
    '''
    os.makedirs(autofz_dir, exist_ok=True)
    crash_dir = os.path.join(autofz_dir, 'crashes')
    hang_dir = os.path.join(autofz_dir, 'hangs')
    queue_dir = os.path.join(autofz_dir, 'queue')
    for d in [crash_dir, hang_dir, queue_dir]:
        os.makedirs(d, exist_ok=True)


def init(target: str, fuzzers: Fuzzers, host_root_dir: Path) -> None:
    for fuzzer in fuzzers:
        if fuzzer not in processed_checksum:
            processed_checksum[fuzzer] = set()
        fuzzer_root_dir = host_root_dir / target / fuzzer
        autofz_dir = fuzzer_root_dir / 'autofz'
        init_dir(autofz_dir)


def import_test_case_dirs(fuzzer_root_dir: Path, input_dir: str) -> List[Path]:
    ret: List[Path] = []
    for queue_dir in pathlib.Path(fuzzer_root_dir).rglob('**/%s' % input_dir):
        queue_dir_s = str(queue_dir)
        if utils.is_dir(queue_dir_s) and f'autofz/{input_dir}' not in str(
                queue_dir):
            logger.debug(queue_dir_s)
            ret.append(Path(queue_dir_s))
    return ret


def import_test_cases(fuzzer_root_dir: Path, input_dir: str) -> List[Path]:
    test_case_dirs: List[Path] = import_test_case_dirs(fuzzer_root_dir,
                                                       input_dir)
    ret: List[Path] = []
    for test_case_dir in test_case_dirs:
        path = test_case_dir / '*'
        test_cases = glob.glob(str(path))
        for test_case in test_cases:
            ret.append(Path(test_case))
    return ret


def new_afl_filename(fuzzer):
    global index
    new_index = None
    if fuzzer not in index:
        index[fuzzer] = 0
    new_index = index[fuzzer]
    index[fuzzer] += 1
    return f'id:{new_index:06d}'


def sync_test_case(target, fuzzer, host_root_dir, testcase):
    fuzzer_config = config['fuzzer'][fuzzer]
    fuzzer_root_dir = os.path.join(host_root_dir, target, fuzzer)
    autofz_dir = os.path.join(fuzzer_root_dir, 'autofz')
    queue_dir = os.path.join(autofz_dir, 'queue')
    # logger.debug(f'copy {testcase.filename} to {queue_dir}')
    new_name = new_afl_filename(fuzzer)
    new_filename = os.path.join(queue_dir, new_name)

    rel_path = os.path.relpath(testcase.filename,
                               os.path.dirname(new_filename))

    # NOTE: every fuzzer will copy file before executing (they should)
    os.symlink(rel_path, new_filename)


def sync2(target: str, fuzzers: Fuzzers, host_root_dir: Path):
    global LAST_INDEX
    global WATCHERS
    # init observer
    # scan all before observer init or make sure observer init first
    init(target, fuzzers, host_root_dir)
    target_config = config['target'][target]

    global_new_test_cases = []
    new_test_cases = nested_dict()

    # handle seeds

    # 1. update global queue
    for fuzzer in fuzzers:
        fuzzer_config = config['fuzzer'][fuzzer]
        fuzzer_root_dir = host_root_dir / target / fuzzer
        new_test_cases[fuzzer] = []
        # NOTE: scan subdir is not as expensive as scan testcases
        # can be optmized when we make sure all the things are setup fist (not scale up)
        if utils.fuzzer_has_subdir(FuzzerType(fuzzer)):
            # print(f'{fuzzer} subdir')
            for subdir in fuzzer_root_dir.iterdir():
                if subdir.is_dir():
                    if subdir.parts[-1] == 'autofz': continue
                    watcher.init_watcher(fuzzer, subdir)
        else:
            watcher.init_watcher(fuzzer, fuzzer_root_dir)
        # not ready
        if fuzzer not in watcher.WATCHERS:
            return

        watchers = watcher.WATCHERS[fuzzer]

        # NOTE: will also synced crashes, which sometimes will also have more coverage
        # read queued testcases
        for w in watchers:
            # prevent iterating while changing
            last_index = LAST_INDEX.get(w, -1)
            queue_len = len(w.test_case_queue)
            for i in range(last_index + 1, queue_len):
                test_case_path = w.test_case_queue[i]
                if w._ignore_test_case(test_case_path):
                    continue
                test_case = TestCase(test_case_path)
                processed_checksum[fuzzer].add(test_case.checksum)
                if test_case.checksum not in global_processed_checksum:
                    global_new_test_cases.append(test_case)
                    global_processed_checksum.add(test_case.checksum)
            LAST_INDEX[w] = queue_len

    # 2. sync to each fuzzer
    for fuzzer in fuzzers:
        # handle new test cases only
        for test_case in global_new_test_cases:
            if test_case.checksum not in processed_checksum[fuzzer]:
                processed_checksum[fuzzer].add(test_case.checksum)
                # do sync!
                sync_test_case(target, fuzzer, host_root_dir, test_case)

    del global_new_test_cases
    del new_test_cases
    # wait some file system writing, doesn't affect our symbolic link but for fuzzers
    time.sleep(0.1)


def test():
    with open('/tmp/test_hash', 'w+') as f:
        f.write('a')
    hash_val = checksum('/tmp/test_hash')
    assert hash_val == 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb'


if __name__ == '__main__':
    test()
