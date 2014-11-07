#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = [line.rstrip() for line in f]

setup(
    name='demoapp',
    install_requires=requirements,
    entry_points={
        'console_scripts': ['app = app:main']
    }
)
