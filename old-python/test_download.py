import download
import unittest
from datetime import *

class TestDownload(unittest.TestCase):

    def test_nomads1(self):
        # make sure the shuffled sequence does not lose any elements
        dt = datetime(2012, 12, 29, 17, 33)
        s=download.make_nomads_suffix(dt)
        self.assertEqual('201212/20121229/nam_218_20121229_1200_003.grb', s)

    def test_nomads2(self):
        dt = datetime(2012, 12, 29, 12)
        s=download.make_nomads_suffix(dt)
        self.assertEqual('201212/20121229/nam_218_20121229_1200_000.grb', s)

    def test_nomads3(self):
        dt = datetime(2012, 12, 29, 0)
        s=download.make_nomads_suffix(dt)
        self.assertEqual('201212/20121229/nam_218_20121229_0000_000.grb', s)

    def test_nomads4(self):
        for hr in range(6, 8):
            dt = datetime(2012, 12, 29, hr)
            s=download.make_nomads_suffix(dt)
            self.assertEqual('201212/20121229/nam_218_20121229_0600_000.grb', s)

    def test_nomads5(self):
        for hr in range(9, 11):
            dt = datetime(2012, 12, 29, hr)
            s=download.make_nomads_suffix(dt)
            self.assertEqual('201212/20121229/nam_218_20121229_0600_003.grb', s)

    def test_local_name(self):
        for hr in range(9, 11):
            dt = datetime(2012, 12, 29, hr)
            s=download.make_local_name(dt)
            self.assertEqual('20121229%02d.grb' % hr, s)
if __name__ == '__main__':
    unittest.main()