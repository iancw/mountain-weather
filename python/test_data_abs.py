from data_abs import *
import unittest
import tempfile
import shutil
from datetime import datetime

class TestGribDatabase(unittest.TestCase):

  def setUp(self):
    self.data_dir = tempfile.mkdtemp()
    self.gd = GribDatabase(self.data_dir)

  def tearDown(self):
    shutil.rmtree(self.data_dir)

  def test_local_hrrr(self):
    dt = datetime(2013, 1, 6, 13)
    self.assertEquals('hrrr_2013_01_06_1300.grb2', self.gd.local_hrrr_name(dt))

  def test_default_levels(self):
    self.assertEquals(6, len(self.gd.params))

if __name__ == '__main__':
  unittest.main()
