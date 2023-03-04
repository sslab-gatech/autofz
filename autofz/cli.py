import os
import sys
from pathlib import Path
from typing import List, Optional

# FIXME
if not __package__:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    __package__ = "autofz"

from tap import Tap

from . import config as Config
from .mytype import Fuzzer

config = Config.CONFIG


class ArgsParser(Tap):
    input: Path
    output: Path
    fuzzer: List[Fuzzer]
    jobs: int
    target: str
    prep: int
    focus: int
    sync: int
    timeout: str
    empty_seed: bool
    crash_mode: str
    enfuzz: int
    focus_one: Optional[str]
    diff_threshold: int
    parallel: bool
    tar: bool

    def configure(self):
        global config
        # NOTE: get default value from config, and overwritable from argv
        DEFAULT_SYNC_TIME = config['scheduler']['sync_time']
        DEFAULT_PREP_TIME = config['scheduler']['prep_time']
        DEFAULT_FOCUS_TIME = config['scheduler']['focus_time']
        available_fuzzers = list(config['fuzzer'].keys())
        available_targets = list(config['target'].keys())

        self.add_argument("--input",
                          "-i",
                          help="Optional input (seed) directory",
                          required=False)
        self.add_argument("--output",
                          "-o",
                          help="An output directory",
                          required=True)
        self.add_argument("--jobs",
                          "-j",
                          help="How many jobs (cores) to use",
                          default=1)
        self.add_argument("--fuzzer",
                          "-f",
                          type=str,
                          nargs='+',
                          choices=available_fuzzers + ['all'],
                          required=True,
                          help="baseline fuzzers to include")
        self.add_argument(
            "--target",
            "-t",
            type=str,
            choices=available_targets,
            required=True,  # only one target allowed
            help="target program to fuzz")
        self.add_argument("--prep",
                          type=int,
                          default=DEFAULT_PREP_TIME,
                          help='prepartion time (Time_{prep})')
        self.add_argument("--focus",
                          type=int,
                          default=DEFAULT_FOCUS_TIME,
                          help='focus time (Time_{focus})')
        self.add_argument("--sync",
                          type=int,
                          default=DEFAULT_SYNC_TIME,
                          help='seed sync interval (used in EnFuzz mode)')
        self.add_argument("--timeout", "-T", default='24h')
        self.add_argument("--empty_seed",
                          "-empty",
                          action="store_true",
                          default=False,
                          help="use empty seed instead")
        self.add_argument("--crash_mode",
                          type=str,
                          choices=['trace', 'ip'],
                          default='ip',
                          help="method to deduplicate bugs.")
        self.add_argument("--enfuzz",
                          type=int,
                          default=None,
                          help="EnFuzz mode, specifiy sync time")
        self.add_argument("--focus-one",
                          default=None,
                          help="Used to run a specific individual fuzzer.")
        self.add_argument("--diff_threshold",
                          type=int,
                          default=100,
                          help="difference threshold (theta_{init} in paper)")
        self.add_argument("--parallel",
                          "-p",
                          action="store_true",
                          default=False,
                          help="parallel mode/multi-core implementaion")
        self.add_argument("--tar",
                          action="store_true",
                          default=False,
                          help="tar fuzzer/eval directories")
