# -*- coding: utf-8 -*-

import unittest

from lakeception import main

class TestMain(unittest.TestCase):
    def test_main(self):
        main.run([u'--test'])
