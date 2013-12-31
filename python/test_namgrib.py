import nam_grib
import unittest
from datetime import *

class TestDownload(unittest.TestCase):

    def test_open(self):
        # make sure the shuffled sequence does not lose any elements
        grb=nam_grib.open('data/nam_218_20130101_0000_000.grb')
        
