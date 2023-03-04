import os
import subprocess
import sys
from abc import ABCMeta, abstractmethod

import psutil

from autofz.common import IS_DEBUG


class FuzzerDriverException(Exception):
    pass


class Fuzzer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class PSFuzzer(Fuzzer):
    def __init__(self, pid, debug=False, debug_file=None):
        self.__pid = pid
        self.debug = debug
        self.debug_file = debug_file

    @property
    def pid(self):
        return self.__pid

    @property
    def proc(self):
        '''
        method to retrive process based on psutils
        '''
        proc = None
        if not self.pid:
            # print('self.pid not exist')
            return None
        if psutil.pid_exists(self.pid):
            proc = psutil.Process(pid=self.pid)
        else:
            # print(f'psutil pid not exist {self.pid}')
            return None
        return proc

    @abstractmethod
    def gen_cwd(self):
        return None

    @abstractmethod
    def gen_run_args(self):
        pass

    def gen_env(self):
        return {}

    def pre_run(self):
        pass

    def run(self):
        if self.proc:
            return
        self.pre_run()
        args = self.gen_run_args()
        cwd = self.gen_cwd()
        env = {**os.environ, **self.gen_env()}
        if IS_DEBUG:
            # print(env)
            print(" ".join(args))
        if self.debug:
            assert self.debug_file
            with open(self.debug_file, 'w+') as f:
                proc = subprocess.Popen(args,
                                        env=env,
                                        cwd=cwd,
                                        stdin=subprocess.DEVNULL,
                                        stdout=f,
                                        stderr=subprocess.STDOUT)
        else:
            proc = subprocess.Popen(args,
                                    env=env,
                                    cwd=cwd,
                                    stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)

        assert proc
        self.__proc = proc
        self.__pid = proc.pid

    def start(self):
        if self.proc:
            # NOTE: alreay start
            print('already started', file=sys.stderr)
            return
        self.run()

    def pause(self):
        if not self.proc:
            raise FuzzerDriverException
        for child in self.proc.children(recursive=True):
            try:
                child.suspend()
            except psutil.NoSuchProcess:
                pass
        self.proc.suspend()

    def resume(self):
        if not self.proc:
            raise FuzzerDriverException
        for child in self.proc.children(recursive=True):
            try:
                child.resume()
            except psutil.NoSuchProcess:
                pass
        self.proc.resume()

    def stop(self):
        if not self.proc:
            # NOTE: no need to raise exception, maybe fuzzer just timeout
            return
        for child in self.proc.children(recursive=True):
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        self.proc.kill()
