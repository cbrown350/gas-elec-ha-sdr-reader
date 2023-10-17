#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    pbr=True,
    setup_requires=['pbr'],
    packages=find_packages(exclude=('test'))
)