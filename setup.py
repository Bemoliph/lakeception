#!/usr/bin/env python2

from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession
import os

from lakeception.const import PROJECT

REQUIREMENTS_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), u'requirements.txt',
    )
)

setup(
    name=PROJECT.NAME,
    description=PROJECT.DESC,
    url=PROJECT.URL,
    version=PROJECT.VERSION,
    test_suite=u'tests',
    packages=find_packages(),
    install_requires=[
        str(i.req)
        for i in parse_requirements(REQUIREMENTS_PATH, session=PipSession())
    ],
    tests_require=[
        u'tox',
        u'coverage',
    ],
    classifiers=[
        u'Development Status :: 2 - Pre-Alpha',
        u'Programming Language :: Python',
        u'Programming Language :: Python :: 2.7',
        u'Topic :: Games/Entertainment :: Arcade',
    ],
)
