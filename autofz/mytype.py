import enum
from pathlib import Path
from typing import Any, Dict, List

from .datatype import Bitmap

Fuzzer = str
Fuzzers = List[Fuzzer]
Coverage = Dict[str, Any]
BitmapContribution = Dict[Fuzzer, Bitmap]


class FuzzerType(enum.Enum):
    AFL = 'afl'
    AFLFAST = 'aflfast'
    MOPT = 'mopt'
    FAIRFUZZ = 'fairfuzz'
    LEARNAFL = 'learnafl'
    RADAMSA = 'radamsa'
    REDQUEEN = 'redqueen'
    LAFINTEL = 'lafintel'
    QSYM = 'qsym'
    ANGORA = 'angora'
    LIBFUZZER = 'libfuzzer'


class SeedType(enum.Enum):
    NORMAL = enum.auto()
    CRASH = enum.auto()
    HANG = enum.auto()


class WatcherConfig:
    def __init__(self, fuzzer: FuzzerType, output_dir: Path):
        self.fuzzer = fuzzer
        self.output_dir = output_dir

    def __eq__(self, other):
        return (self.fuzzer == other.fuzzer
                and self.output_dir.resolve() == other.output_dir.resolve())

    def __hash__(self):
        return hash(self.fuzzer.value + str(self.output_dir.resolve()))


def test():
    assert FuzzerType('afl')


if __name__ == '__main__':
    test()
