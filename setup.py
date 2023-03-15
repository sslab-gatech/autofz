#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

# packages = find_packages()
packages = ['autofz', 'autofz.fuzzer_driver', 'draw']

# https://github.com/google-research/arxiv-latex-cleaner/blob/main/setup.py

install_requires = []
with open("requirements.txt") as f:
    for l in f.readlines():
        l_c = l.strip()
        if l_c and not l_c.startswith('#'):
            install_requires.append(l_c)

setup(
    name='autofz',
    version='0.1',
    description="a meta fuzzer for automated fuzzer composition at runtime",
    packages=packages,
    url='https://github.com/sslab-gatech/autofz',
    author="Yu-Fu Fu",
    author_email="yufu@gatech.edu",
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['autofz = autofz.main:main',
                            'autofz-draw = draw.draw_main:main'],
    },
    package_data={'autofz': ['aflforkserver.so']},
    python_requires=">=3.9.4",
)
