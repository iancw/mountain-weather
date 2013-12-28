import download
import unittest
from datetime import *
import fetch_hrrr

class TestFetch(unittest.TestCase):

  def test_dt(self):
    self.assertEquals('201312261700', fetch_hrrr.time_format(datetime(2013, 12, 26, 17)))

  def test_url(self):
    self.assertEquals('hrrr.2d.201312261700f000.grib2', fetch_hrrr.leaf_file(datetime(2013, 12, 26, 17)))

  def test_partial_path(self):
    dt = datetime(2013, 12, 26, 17)
    self.assertEquals('201312261700/hrrr.2d.201312261700f000.grib2', fetch_hrrr.sub_path(dt))

if __name__ == '__main__':
  unittest.main()
