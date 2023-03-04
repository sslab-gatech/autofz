import os
import pathlib
import sys
import time

import peewee
import psutil
from autofz import config as Config

from .db import AFLModel, ControllerModel, db_proxy
from .fuzzer import FuzzerDriverException, PSFuzzer

CONFIG = Config.CONFIG
FUZZER_CONFIG = CONFIG['fuzzer']


def parse_fuzzer_stats(fuzzer_stats_file):
    ret = {}
    if not os.path.exists(fuzzer_stats_file):
        return None
    with open(fuzzer_stats_file) as f:
        for l in f:
            arr = l.split(":")
            key = arr[0].strip()
            value = arr[1].strip()
            ret[key] = value
    assert ret
    return ret


class AFLBase(PSFuzzer):
    def __init__(self,
                 seed,
                 output,
                 group,
                 program,
                 argument,
                 master=True,
                 cgroup_path='',
                 fuzzer_id=0,
                 pid=None):
        '''
        fuzzer_id used to distinguish different slaves
        '''
        super().__init__(pid)
        self.seed = seed
        self.output = output
        self.group = group
        self.program = program
        self.argument = argument
        self.master = master
        self.cgroup_path = cgroup_path
        self.fuzzer_id = fuzzer_id
        self.__fuzzer_stats = None
        self.__proc = None

    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['afl']['command']

    @property
    def name(self):
        if self.master:
            return f'{Config.AFL_MASTER_STR}_{self.fuzzer_id}'
        else:
            return f'{Config.AFL_SLAVE_STR}_{self.fuzzer_id}'

    def update_fuzzer_stats(self):
        fuzzer_stats_file = f'{self.output}/{self.name}/fuzzer_stats'
        self.__fuzzer_stats = parse_fuzzer_stats(fuzzer_stats_file)

    @property
    def fuzzer_stats(self):
        if self.__fuzzer_stats is None:
            self.update_fuzzer_stats()
        return self.__fuzzer_stats

    @property
    def is_master(self):
        return self.master

    @property
    def is_slave(self):
        return not self.is_master

    @property
    def is_active(self):
        return self.proc.status() != psutil.STATUS_STOPPED

    @property
    def is_inactive(self):
        return self.proc.status() == psutil.STATUS_STOPPED

    @property
    def is_ready(self):
        queue_dir = f'{self.output}/{self.name}/queue'
        return os.path.exists(queue_dir)

    @property
    def target(self):
        global FUZZER_CONFIG
        target_root = FUZZER_CONFIG['afl']['target_root']
        return os.path.join(target_root, self.group, self.program,
                            self.program)

    def gen_cwd(self):
        return os.path.dirname(self.target)

    def gen_env(self):
        return {
            'AFL_NO_UI': '1',
            'AFL_SKIP_CPUFREQ': '1',
            'AFL_NO_AFFINITY': '1',
            'AFL_SKIP_CRASHES': '1',  # some seed make asan-compiled crash
            'AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES': '1',
            'AFL_SHUFFLE_QUEUE': '1'
        }

    def check(self):
        ret = True
        ret &= os.path.exists(self.target)
        if not ret:
            raise FuzzerDriverException

    def gen_run_args(self):
        self.check()

        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class AFLPPBase(PSFuzzer):
    def __init__(self,
                 seed,
                 output,
                 group,
                 program,
                 argument,
                 master=True,
                 cgroup_path='',
                 fuzzer_id=0,
                 pid=None):
        '''
        fuzzer_id used to distinguish different slaves
        '''
        super().__init__(pid)
        self.seed = seed
        self.output = output
        self.group = group
        self.program = program
        self.argument = argument
        self.master = master
        self.cgroup_path = cgroup_path
        self.fuzzer_id = fuzzer_id
        self.__fuzzer_stats = None
        self.__proc = None

    @property
    def afl_command(self):
        raise NotImplementedError

    @property
    def name(self):
        if self.master:
            return f'{Config.AFL_MASTER_STR}_{self.fuzzer_id}'
        else:
            return f'{Config.AFL_SLAVE_STR}_{self.fuzzer_id}'

    def update_fuzzer_stats(self):
        fuzzer_stats_file = f'{self.output}/{self.name}/fuzzer_stats'
        self.__fuzzer_stats = parse_fuzzer_stats(fuzzer_stats_file)

    @property
    def fuzzer_stats(self):
        if self.__fuzzer_stats is None:
            self.update_fuzzer_stats()
        return self.__fuzzer_stats

    @property
    def is_master(self):
        return self.master

    @property
    def is_slave(self):
        return not self.is_master

    @property
    def is_active(self):
        return self.proc.status() != psutil.STATUS_STOPPED

    @property
    def is_inactive(self):
        return self.proc.status() == psutil.STATUS_STOPPED

    @property
    def is_ready(self):
        queue_dir = f'{self.output}/{self.name}/queue'
        return os.path.exists(queue_dir)

    @property
    def target(self):
        raise NotImplementedError

    def gen_cwd(self):
        return os.path.dirname(self.target)

    def gen_env(self):
        return {
            'AFL_NO_UI': '1',
            'AFL_SKIP_CPUFREQ': '1',
            'AFL_NO_AFFINITY': '1',
            'AFL_SKIP_CRASHES': '1',  # some seed make asan-compiled crash
            'AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES': '1',
            'AFL_SHUFFLE_QUEUE': '1'
        }

    def check(self):
        ret = True
        ret &= os.path.exists(self.target)
        if not ret:
            raise FuzzerDriverException

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class AFL(AFLBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['afl']['command']

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class AFLFAST(AFLBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['aflfast']['command']

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        if self.master:
            args += ['-p', 'fast']
        else:
            # NOTE: different scheduler when we launch multiple instances
            idx = self.fuzzer_id % 3
            if idx == 0:
                args += ['-p', 'fast']
            elif idx == 1:
                args += ['-p', 'coe']
            elif idx == 2:
                args += ['-p', 'explore']
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class MOPT(AFLBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['mopt']['command']

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-L', '1']  # recommended by authors
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class FAIRFUZZ(AFLBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['fairfuzz']['command']

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class LEARNAFL(AFLBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['learnafl']['command']

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class LAFINTEL(AFLPPBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['lafintel']['command']

    @property
    def target(self):
        global FUZZER_CONFIG
        target_root = FUZZER_CONFIG['lafintel']['target_root']
        return os.path.join(target_root, self.group, self.program,
                            self.program)

    def gen_cwd(self):
        return os.path.dirname(self.target)

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class REDQUEEN(AFLPPBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['redqueen']['command']

    @property
    def target(self):
        global FUZZER_CONFIG
        target_root = FUZZER_CONFIG['redqueen']['target_root']
        return os.path.join(target_root, self.group, self.program,
                            self.program)

    @property
    def target_cmp(self):
        global FUZZER_CONFIG
        target_root = FUZZER_CONFIG['redqueen']['target_root_cmp']
        return os.path.join(target_root, self.group, self.program,
                            self.program)

    def gen_cwd(self):
        return os.path.dirname(self.target)

    def check(self):
        ret = True
        ret &= os.path.exists(self.target)
        ret &= os.path.exists(self.target_cmp)
        if not ret:
            raise FuzzerDriverException

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['-c', self.target_cmp]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class RADAMSA(AFLPPBase):
    @property
    def afl_command(self):
        global FUZZER_CONFIG
        return FUZZER_CONFIG['radamsa']['command']

    @property
    def target(self):
        global FUZZER_CONFIG
        target_root = FUZZER_CONFIG['radamsa']['target_root']
        return os.path.join(target_root, self.group, self.program,
                            self.program)

    def gen_cwd(self):
        return os.path.dirname(self.target)

    # AFL++
    def gen_env(self):
        global FUZZER_CONFIG
        aflpp_dir = FUZZER_CONFIG['radamsa']['aflpp_dir']
        SONAME = os.path.join(aflpp_dir, "custom_mutators", "radamsa",
                              "radamsa-mutator.so")

        return {
            **super().gen_env(),
            'AFL_CUSTOM_MUTATOR_LIBRARY': SONAME,
            'AFL_CUSTOM_MUTATOR_ONLY': '1'  # will skip afl deterministic
        }

    def gen_run_args(self):
        self.check()
        args = []
        if self.cgroup_path:
            args += ['cgexec', '-g', f'cpu:{self.cgroup_path}']
        args += [self.afl_command, '-i', self.seed, '-o', self.output]
        args += ['-m', 'none']
        args += ['-t', '1000+']
        args += ['-M'] if self.master else ['-S']
        args += [self.name]
        args += ['--', self.target]
        args += self.argument.split(' ')
        return args


class AFLBasedController(ControllerModel):
    def __init__(self, AFLClass, name, seed, output, group, program, argument,
                 cgroup_path):
        self.AFLClass = AFLClass
        self.name = name
        self.db = None
        self.seed = seed
        self.output = output
        self.group = group
        self.program = program
        self.argument = argument
        self.cgroup_path = cgroup_path
        self.afls = []

    def init(self):
        db_proxy.initialize(self.db)
        self.db.connect()
        self.db.create_tables([AFLModel, ControllerModel])

        for fuzzer in AFLModel.select():
            # print(fuzzer.fuzzer_id)
            afl = self.AFLClass(seed=fuzzer.seed,
                                output=fuzzer.output,
                                group=fuzzer.group,
                                program=fuzzer.program,
                                argument=fuzzer.argument,
                                master=fuzzer.master,
                                fuzzer_id=fuzzer.fuzzer_id,
                                cgroup_path=self.cgroup_path,
                                pid=fuzzer.pid)
            self.afls.append(afl)

    def get_master(self):
        for AFL in self.afls:
            if AFL.is_master:
                return AFL

    def get_current_active(self):
        active = []
        for afl in self.afls:
            if afl.is_active:
                active.append(afl)
        return active

    def get_current_inactive(self):
        inactive = []
        for afl in self.afls:
            if afl.is_inactive:
                inactive.append(afl)
        return inactive

    def start(self):
        if self.afls:
            print('already started', file=sys.stderr)
            return
        afl = self.AFLClass(seed=self.seed,
                            output=self.output,
                            group=self.group,
                            program=self.program,
                            argument=self.argument,
                            cgroup_path=self.cgroup_path,
                            master=True,
                            fuzzer_id=1)
        afl.start()
        while not afl.is_ready:
            time.sleep(1)
        AFLModel.create(seed=self.seed,
                        output=self.output,
                        group=self.group,
                        program=self.program,
                        argument=self.argument,
                        master=True,
                        pid=afl.pid,
                        fuzzer_id=1)
        ControllerModel.create(scale_num=1)
        ready_path = os.path.join(self.output, 'ready')
        pathlib.Path(ready_path).touch(mode=0o666, exist_ok=True)

    def scale(self, scale_num):
        if not self.afls:
            print('start first', file=sys.stderr)
            return
        num = scale_num
        assert num >= 0
        current_active = self.get_current_active()
        current_inactive = self.get_current_inactive()
        current_active_num = len(current_active)
        current_inactive_num = len(current_inactive)
        master = self.get_master()
        if current_active_num < num:
            # scale up
            diff = num - current_active_num
            # first resume inative
            resume_num = min(diff, current_inactive_num)
            resumed = 0

            if resume_num and master.is_inactive:
                master.resume()
                resumed += 1

            for afl in current_inactive:
                if resumed == resume_num: break
                if afl.is_active: continue
                afl.resume()
                resumed += 1

            start_id = len(self.afls) + 1
            for i in range(start_id, start_id + diff - resume_num):
                afl = self.AFLClass(seed=self.seed,
                                    output=self.output,
                                    group=self.group,
                                    program=self.program,
                                    argument=self.argument,
                                    master=False,
                                    cgroup_path=self.cgroup_path,
                                    fuzzer_id=i)
                afl.start()
                AFLModel.create(seed=self.seed,
                                output=self.output,
                                group=self.group,
                                program=self.program,
                                argument=self.argument,
                                master=False,
                                pid=afl.pid,
                                fuzzer_id=i)
        elif current_active_num > num:
            # scale down
            diff = current_active_num - num
            # pause slave first
            paused = 0
            for afl in current_active:
                if paused == diff: break
                if num >= 1 and afl.is_master:
                    continue
                afl.pause()
                paused += 1
        else:
            # print('does not need to scale', file=sys.stderr)
            return
        controller = ControllerModel.get()
        controller.scale_num = scale_num
        controller.save()

    def pause(self):
        for afl in self.afls:
            afl.pause()

    def resume(self):
        '''
        NOTE: prserve scaling
        '''
        controller = ControllerModel.get()
        self.scale(controller.scale_num)

    def stop(self):
        for afl in self.afls:
            afl.stop()
        self.db.drop_tables([AFLModel, ControllerModel])


class AFLController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(AFL, 'afl', seed, output, group, program, argument,
                         cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-afl.db'))


class AFLFASTController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(AFLFAST, 'aflfast', seed, output, group, program,
                         argument, cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-aflfast.db'))


class MOPTController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(MOPT, 'mopt', seed, output, group, program, argument,
                         cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-mopt.db'))


class FAIRFUZZController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(FAIRFUZZ, 'fairfuzz', seed, output, group, program,
                         argument, cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-fairfuzz.db'))


class LAFINTELController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(LAFINTEL, 'lafintel', seed, output, group, program,
                         argument, cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-lafintel.db'))


class LEARNAFLController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(LEARNAFL, 'learnafl', seed, output, group, program,
                         argument, cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-learnafl.db'))


class REDQUEENController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(REDQUEEN, 'redqueen', seed, output, group, program,
                         argument, cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-redqueen.db'))


class RADAMSAController(AFLBasedController):
    def __init__(self, seed, output, group, program, argument, thread,
                 cgroup_path):
        super().__init__(RADAMSA, 'radamsa', seed, output, group, program,
                         argument, cgroup_path)
        self.db = peewee.SqliteDatabase(
            os.path.join(Config.DATABASE_DIR, 'autofz-radamsa.db'))
