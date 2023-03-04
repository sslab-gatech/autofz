#!/usr/bin/env python3
import logging
import os

from . import config as Config
from .common import nested_dict

config = Config.CONFIG

logger = logging.getLogger('autofz.fuzzing')

log = nested_dict()

containers = nested_dict()


def check(target, fuzzer, host_output):
    fuzzer_config = config['fuzzer'][fuzzer]
    target_config = config['target'][target]
    basename = fuzzer
    assert basename
    create_output_dir = fuzzer_config.get('create_output_dir', True)

    unsupported = target_config.get('unsupported', [])

    if fuzzer in unsupported:
        logger.error(f'{target} does not support {fuzzer}')
        return False

    if create_output_dir:
        return True
    else:
        host_output_dir = f'{host_output}/{target}'
        if os.path.exists(f'{host_output_dir}/{basename}'):
            logger.error(f'Please remove {host_output_dir}/{basename}')
            return False
        return True
