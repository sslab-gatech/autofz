import os
import pathlib
import sys
import time

import peewee
# from .. import config as Config
from autofz import config as Config

from . import afl
from .controller import Controller
from .db import AngoraModel, ControllerModel, db_proxy
from .fuzzer import FuzzerDriverException, PSFuzzer

CONFIG = Config.CONFIG
FUZZER_CONFIG = CONFIG['fuzzer']

class Angora(PSFuzzer):
    def __init__(self,
                 seed,
                 output,
                 group,
                 program,
                 argument,
                 thread=1,
                 pid=None,
                 cgroup_path = ''):
        '''
        fuzzer_id used to distinguish different slaves
        '''
        debug_file=os.path.realpath(os.path.join(output,'..','..','autofz_angora.log'))
        debug = False
        super().__init__(pid, debug=debug, debug_file=debug_file)
        self.seed = seed
        self.output = output
        self.group = group
        self.program = program
        self.argument = argument
        self.name = 'angora'
        self.thread = thread
        self.cgroup_path = cgroup_path
        self.__proc = None
        self.__fuzzer_stats = None

    def update_fuzzer_stats(self):
        fuzzer_stats_file = f'{self.output}/angora/fuzzer_stats'
        self.__fuzzer_stats = afl.parse_fuzzer_stats(fuzzer_stats_file)

    @property
    def fuzzer_stats(self):
        if self.__fuzzer_stats is None:
            self.update_fuzzer_stats()
        return self.__fuzzer_stats

    @property
    def pid_(self):
        if not self.fuzzer_stats: return None
        return int(self.fuzzer_stats['fuzzer_pid'])

    @property
    def is_ready(self):
        return self.fuzzer_stats is not None

    def gen_env(self):
        LD_LIBRARY_PATH = os.environ.get('LD_LIBRARY_PATH')
        NEW_PATH = f'/fuzzer/angora/clang+llvm/lib:{LD_LIBRARY_PATH}'
        return {'ANGORA_DISABLE_CPU_BINDING': '1',
                'LD_LIBRARY_PATH':NEW_PATH}

    @property
    def target(self):
        global FUZZER_CONFIG
        target_root = FUZZER_CONFIG['angora']['target_root']
        return os.path.join(target_root, self.group,self.program,self.program)

    @property
    def target_taint(self):
        global FUZZER_CONFIG
        target_root = FUZZER_CONFIG['angora']['target_root_taint']
        return os.path.join(target_root, self.group,self.program,self.program)

    def gen_cwd(self):
        return os.path.dirname(self.target)

    def check(self):
        ret = True
        ret &= os.path.exists(self.target)
        ret &= os.path.exists(self.target_taint)
        if not ret:
            raise FuzzerDriverException


    def gen_run_args(self):
        self.check()
        global FUZZER_CONFIG
        command = FUZZER_CONFIG['angora']['command']
        args = []
        if self.cgroup_path:
            args += ['cgexec','-g',f'cpu:{self.cgroup_path}']
        args += [command]
        args += ['-M', str(0)]
        args += ['--jobs', str(self.thread)]
        args += ['-S']
        args += ['--input', self.seed]
        args += ['--output', self.output]
        args += [
            '-t',
            self.target_taint
        ]
        args += [
            '--',
            self.target
        ]
        args += self.argument.split(' ')
        return args


class ANGORAController(Controller):
    def __init__(self, seed, output, group, program, argument, thread=1, cgroup_path=''):
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-angora.db'))
        self.name = 'angora'
        self.seed = seed
        self.output = output
        self.group = group
        self.program = program
        self.argument = argument
        self.thread = thread
        self.cgroup_path = cgroup_path
        self.angoras = []
        self.kwargs = {
            'seed': self.seed,
            'output': self.output,
            'group': self.group,
            'program': self.program,
            'argument': self.argument,
            'thread': self.thread,
            'cgroup_path' : self.cgroup_path
        }

    def init(self):
        db_proxy.initialize(self.db)
        self.db.connect()
        self.db.create_tables([AngoraModel, ControllerModel])

        for fuzzer in AngoraModel.select():
            angora = Angora(seed=fuzzer.seed,
                            output=fuzzer.output,
                            group=fuzzer.group,
                            program=fuzzer.program,
                            argument=fuzzer.argument,
                            thread=fuzzer.thread,
                            pid=fuzzer.pid)
            self.angoras.append(angora)

    def start(self):
        if self.angoras:
            print('already started', file=sys.stderr)
            return
        # start Angora
        angora = Angora(**self.kwargs)
        angora.start()
        # wait angora pid
        while not angora.is_ready:
            time.sleep(1)
        AngoraModel.create(**self.kwargs, pid=angora.pid_)
        ControllerModel.create(scale_num=1)
        time.sleep(10)
        ready_path = os.path.join(self.output, 'ready')
        pathlib.Path(ready_path).touch(mode=0o666, exist_ok=True)

    def scale(self, scale_num):
        '''
        NOTE: angora uses thread model
        '''
        pass

    def pause(self):
        for angora in self.angoras:
            angora.pause()

    def resume(self):
        '''
        NOTE: prserve scaling
        '''
        controller = ControllerModel.get()
        for angora in self.angoras:
            angora.resume()

    def stop(self):
        for angora in self.angoras:
            angora.stop()
        self.db.drop_tables([AngoraModel, ControllerModel])
