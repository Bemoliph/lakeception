
import unittest

from lakeception import main

class TestBiome(unittest.TestCase):
    def test_main(self):
        main(["--test"])
