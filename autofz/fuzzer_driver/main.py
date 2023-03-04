#!/usr/bin/env python3
import argparse
import os
import sys

# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .afl import (AFLController, AFLFASTController, FAIRFUZZController,
                  LAFINTELController, LEARNAFLController, MOPTController,
                  RADAMSAController, REDQUEENController)
from .angora import ANGORAController
from .libfuzzer import LIBFUZZERController
from .qsym import QSYMController


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname, None)


def parse_args(raw_args=None):
    p = argparse.ArgumentParser()
    p.add_argument("-i",
                   "--input",
                   type=str,
                   help="afl input/seed dir",
                   required=True)
    p.add_argument("-o",
                   "--output",
                   type=str,
                   help="afl output dir",
                   required=True)
    p.add_argument("-j", "--jobs", type=int, help="thread number", default=1)
    p.add_argument("-g",
                   "--group",
                   type=str,
                   help="group",
                   choices=['unibench', 'lava', 'fuzzer-test-suite'],
                   required=True)
    p.add_argument("-p", "--program", type=str, help="program", required=True)
    p.add_argument("--args", type=str, help="program argument", required=True)
    p.add_argument("-f", "--fuzzer", type=str, help="fuzzer", required=True)
    sp = p.add_subparsers(dest='command', help="command", required=True)
    sp.add_parser('start')
    sp.add_parser('stop')
    sp.add_parser('pause')
    sp.add_parser('resume')
    p_scale = sp.add_parser('scale')
    p_scale.add_argument('scale_num', type=int)
    return p.parse_args(raw_args)


def main(fuzzer,
         seed,
         output,
         group,
         program,
         argument,
         thread,
         command,
         cgroup_path='',
         scale_num=1):
    controller_class = str_to_class(f'{str.upper(fuzzer)}Controller')
    if controller_class is None:
        print(f"{fuzzer} controller doesn't exist.")

    controller = controller_class(seed=os.path.realpath(seed),
                                  output=os.path.realpath(output),
                                  group=group,
                                  program=program,
                                  argument=argument,
                                  thread=thread,
                                  cgroup_path=cgroup_path)
    controller.init()
    command = command

    if command == 'start':
        controller.start()
    elif command == 'stop':
        controller.stop()
    elif command == 'pause':
        controller.pause()
    elif command == 'resume':
        controller.resume()
    elif command == 'scale':
        controller.scale(scale_num)


if __name__ == '__main__':
    args = parse_args()
    main(fuzzer=args.fuzzer,
         seed=args.input,
         output=os.path.realpath(args.output),
         group=args.group,
         program=args.program,
         argument=args.args,
         thread=args.jobs,
         command=args.command,
         scale_num=args.scale_num)
