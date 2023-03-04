#!/usr/bin/env python3
import logging
import os
import time

import numpy as np
from bitarray import bitarray

logger = logging.getLogger('autofz.datatype')
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


class Bitmap(object):
    # NOTE: copy from cupid, but we actually use only use 16 bits during fuzzing (/d/p/justafl/)
    BITMAP_SIZE = 1048576

    def __init__(self, bitmap=None, bitmap_path=None):
        if bitmap is not None:
            self.bitmap = bitmap
            return
        assert bitmap_path
        self.bitmap = None
        counter = 0
        while os.stat(bitmap_path).st_size != Bitmap.BITMAP_SIZE:
            time.sleep(0.1)
            if counter > 100:
                break
            counter += 1
        if counter:
            logger.critical(f'bitmap counter: {counter}')
        with open(bitmap_path, 'rb') as f:
            content = f.read()
            self.bitmap = np.array(bytearray(content), dtype='uint8')
            # has beed normalized by quickcov
        assert self

    @classmethod
    def empty(cls):
        b = bytearray([0]) * cls.BITMAP_SIZE
        bitmap = np.array(b)
        del b
        return cls(bitmap=bitmap)

    @classmethod
    def full(cls):
        b = bytearray([1]) * cls.BITMAP_SIZE
        bitmap = np.array(b)
        del b
        return cls(bitmap=bitmap)

    def __bool__(self):
        return self.bitmap is not None

    def normalize_bitmap(self):
        # it could be an AFL virgin_bits or an AFL trace_bits
        # virgin_bits uses 0xff to say "this edge was not touched"
        # trace_bits uses 0x00 to say the same
        # so only count an edge as visited if it's neither 0xff nor 0x00
        # more reliant than trying to detect if it's coming from virgin_bits or trace_bits
        self.bitmap = np.array(np.where(
            (self.bitmap != 0xff) & (self.bitmap != 0x00), 1, 0),
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
        # print(self.bitmap)
        # print(np.sum(self.bitmap))
        return int(np.sum(self.bitmap))

    # use other bitmap as baseline, what are the new branches in our bitmap?
    def delta(self, other):
        if len(other.bitmap) > 0:
            self.initialize_bitmap_if_necessary(len(other.bitmap))
        elif len(self.bitmap) > 0:
            other.initialize_bitmap_if_necessary(len(self.bitmap))
        assert (len(self.bitmap) == len(other.bitmap))
        delta = (self.bitmap | other.bitmap) - other.bitmap
        return Bitmap(bitmap=delta)

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
        return Bitmap(u)

    def intersect(self, other):
        if len(other.bitmap) == 0:
            return
        self.initialize_bitmap_if_necessary(len(other.bitmap))
        assert (len(self.bitmap) == len(other.bitmap))
        u = self.bitmap & other.bitmap
        return Bitmap(u)

    def __lt__(self, other):
        return other.delta_count(self) > 0

    def __gt__(self, other):
        return self.delta_count(other) > 0

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersect(other)

    def __sub__(self, other):
        return self.delta(other)

    def __add__(self, other):
        return self.union(other)

    def toJSON(self):
        return {'count': self.count()}

    def __repr__(self):
        return str({'count': self.count(), 'size': len(self.bitmap)})

    def __copy__(self):
        return Bitmap(bitmap=self.bitmap)

    def __deepcopy__(self, memo):
        return Bitmap(bitmap=self.bitmap)


class Bugmap(object):
    BUG_MAP_SIZE = 2**20

    def __init__(self, bug_map=None, bug_map_path=None):
        self.bug_map = None
        if bug_map is not None:
            self.bug_map = bug_map
        elif bug_map_path:
            self.bug_map = bitarray()
            counter = 0
            while os.stat(bug_map_path).st_size != 131072:
                time.sleep(0.1)
                if counter > 100:
                    break
            if counter:
                logger.critical(f'bug map counter: {counter}')
            with open(bug_map_path, 'rb') as f:
                self.bug_map.fromfile(f)
        assert self

    def __bool__(self):
        return self.bug_map is not None

    @classmethod
    def empty(cls):
        empty_bm = bitarray(cls.BUG_MAP_SIZE)
        empty_bm.setall(False)
        return cls(bug_map=empty_bm)

    @classmethod
    def full(cls):
        full_bm = bitarray(cls.BUG_MAP_SIZE)
        full_bm.setall(True)
        return cls(bug_map=full_bm)

    @classmethod
    def count(self):
        return self.bug_map.count(True)

    def delta(self, other):
        u = self.union(other)
        d = u ^ other
        return Bugmap(bug_map=d)

    def union(self, other):
        return Bugmap(bug_map=self.bug_map | other.bug_map)

    def intersect(self, other):
        return Bugmap(bug_map=self.bug_map & other.bug_map)

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersect(other)

    def __sub__(self, other):
        return self.delta(other)

    def __add__(self, other):
        return self.union(other)

    def toJSON(self):
        return {'count': self.count()}

    def __repr__(self):
        return str({'count': self.count(), 'size': len(self.bug_map)})

    def __copy__(self):
        return Bugmap(bug_map=self.bug_map)

    def __deepcopy__(self, memo):
        return Bugmap(bug_map=self.bug_map)


def test_bitmap():
    print(Bitmap.BITMAP_SIZE)
    empty_bitmap = Bitmap.empty()
    bitmap_path = os.path.join(SCRIPT_PATH, 'tests', 'data', 'bitmap')
    bm = Bitmap(bitmap_path=bitmap_path)
    print(bm)
    print(len(bm.bitmap))
    b = bytearray([0]) * len(bm.bitmap)
    bitmap = np.array(b)
    empty_bitmap += bm
    print(empty_bitmap)


def test_bugmap():
    print(Bugmap.BUG_MAP_SIZE)
    empty_bm = Bugmap.empty()
    print(empty_bm)
    bug_map_path = os.path.join(SCRIPT_PATH, 'tests', 'data', 'bug_map')
    bm = Bugmap(bug_map_path=bug_map_path)


def main():
    test_bitmap()
    test_bugmap()


if __name__ == '__main__':
    main()
