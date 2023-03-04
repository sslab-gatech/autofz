'''
implement different scheduling polcies
'''
import logging
from abc import ABCMeta, abstractmethod

import toolz

from . import config as Config

config = Config.CONFIG

logger = logging.getLogger('autofz.policy')


class Policy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def schedule(self):
        pass

    @abstractmethod
    def calculate_cpu(self, fuzzers, fuzzer_info=None, max_cores=1):
        pass


class BitmapPolicy(Policy):
    def __init__(self):
        pass

    def schedule(self):
        pass

    def _check(self, fuzzers, fuzzer_info):
        fuzzers_bitmap = fuzzer_info['bitmap']
        return fuzzers_bitmap is not None

    def _rank(self, fuzzers, fuzzer_info):
        fuzzers_bitmap = fuzzer_info['bitmap']
        fuzzers_bitmap_count = toolz.valmap(lambda x: x.count(),
                                            fuzzers_bitmap)
        array_bitmap = list(fuzzers_bitmap_count.items())
        sorted_bitmap = sorted(array_bitmap, key=lambda t: t[1], reverse=True)
        prev_coverage = 2**32
        now_rank = -1
        now_rank_num = 0
        rank = {}
        rank_num = {}
        ordered_fuzzers = []
        for f, cov in sorted_bitmap:
            # NOTE: handle repetitive element
            ordered_fuzzers.append(f)
            val = cov
            if prev_coverage > val:
                now_rank_num = 1
                now_rank += 1
            elif prev_coverage == val:
                now_rank_num += 1
            rank[f] = now_rank
            rank_num[now_rank] = now_rank_num
            prev_coverage = val
        return rank, rank_num, ordered_fuzzers

    def calculate_cpu(self, fuzzers, fuzzer_info, max_cores=1):
        if not self._check(fuzzers, fuzzer_info):
            return None
        rank, rank_num, ordered_fuzzers = self._rank(fuzzers, fuzzer_info)
        cpu_assign = {}
        picked_fuzzers = []
        for fuzzer in fuzzers:
            if rank[fuzzer] == 0:
                # NOTE: allow fraction
                picked_fuzzers.append(fuzzer)
                cpu_assign[fuzzer] = max_cores / rank_num[0]
            else:
                cpu_assign[fuzzer] = 0
        return picked_fuzzers, cpu_assign

    def calculate_cpu_with_last(self,
                                fuzzers,
                                fuzzer_info,
                                last_picked_fuzzers,
                                max_cores=1):
        if not self._check(fuzzers, fuzzer_info):
            return None
        rank, rank_num, ordered_fuzzers = self._rank(fuzzers, fuzzer_info)
        cpu_assign = {}
        picked_fuzzers = []
        picked_fuzzers_new = []
        # total share
        total = rank_num[0] + len(last_picked_fuzzers)

        # this round
        for fuzzer in fuzzers:
            # 0 means with top bitmap, might have multiple one
            if rank[fuzzer] == 0:
                share = 1
                picked_fuzzers_new.append(fuzzer)
            else:
                share = 0
            if fuzzer in last_picked_fuzzers:
                share += 1
            # NOTE: allow fraction
            if share > 0:
                picked_fuzzers.append(fuzzer)
                cpu_assign[fuzzer] = max_cores * (share / total)
            else:
                cpu_assign[fuzzer] = 0

        return picked_fuzzers, cpu_assign, picked_fuzzers_new

    def ordered_fuzzers(self, fuzzers, fuzzer_info):
        if not self._check(fuzzers, fuzzer_info):
            return None
        rank, rank_num, ordered_fuzzers = self._rank(fuzzers, fuzzer_info)
        return ordered_fuzzers
