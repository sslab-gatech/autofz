#!/usr/bin/env python3
import collections
import logging
import os
import sys

import coloredlogs

# FIXME
if not __package__:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    __package__ = "autofz"


def nested_dict():
    return collections.defaultdict(nested_dict)


LOGGER_FORMAT = '%(asctime)s :: %(levelname)-5s :: %(name)s :: %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOGGER_FIELD_STYLES = {
    'asctime': {
        'color': 'green'
    },
    'hostname': {
        'color': 'magenta'
    },
    'levelname': {
        'bold': True,
        'color': 'white'
    },
    'name': {
        'color': 'blue'
    },
    'programname': {
        'color': 'cyan'
    },
    'username': {
        'color': 'yellow'
    }
}

IS_DEBUG = False

IS_PROFILE = 'PROFILE' in os.environ

logger = logging.getLogger('autofz')

if 'DEBUG' in os.environ:
    coloredlogs.install(level=logging.DEBUG,
                        fmt=LOGGER_FORMAT,
                        field_styles=LOGGER_FIELD_STYLES,
                        logger=logger)
    IS_DEBUG = True
else:
    coloredlogs.install(level=logging.INFO,
                        fmt=LOGGER_FORMAT,
                        field_styles=LOGGER_FIELD_STYLES,
                        logger=logger)
