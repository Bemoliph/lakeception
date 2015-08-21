#!/usr/bin/env python2

from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession
import os

REQUIREMENTS_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "requirements.txt",
    )
)

setup(
    name="lakeception",
    url="https://github.com/bemoliph/lakeception",
    version="0.0.1",
    test_suite="tests",
    packages=find_packages(),
    install_requires=[
        str(i.req)
        for i in parse_requirements(REQUIREMENTS_PATH, session=PipSession())
    ],
    dependency_links=[
        "hg+https://bitbucket.org/pygame/pygame#egg=pygame-dev",
    ],
    tests_require=[
        "tox",
        "coverage",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console :: Curses",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Games/Entertainment :: Arcade",
    ],
)
