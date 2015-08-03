
import unittest

from lakeception import main

class TestMain(unittest.TestCase):
    def test_main(self):
        main.main(["--test"])
