import os
import os.path
import urllib2
from datetime import *

def url_root():
  return 'http://hrrr.agron.iastate.edu/data/hrrr/'

def time_format(dt):
  return dt.strftime('%Y%m%d%H%M')

# e.g. 201312031000/
# followed by...
# hrrr.2d.201312270500f000.grib2
# hrrr.2d.201312270500f001.grib2
# hrrr.2d.2013 12 27 05 00 f001.grib2
# suffixes include f000 through f011
def leaf_file(dt):
  return 'hrrr.2d.{0}f000.grib2'.format(time_format(dt))

def sub_path(dt):
  return '{0}/{1}'.format(time_format(dt), leaf_file(dt))

def build_path(dt):
  return '{0}{1}'.format(url_root(), sub_path(dt))

def download_time(dt):
  path=build_path(dt)
  file_name = leaf_file(dt)
  if os.path.exists(os.path.join('.', file_name)):
    print "File {0} already present, returning".format(path)
    return file_name
  print "Downloading {0}".format(path)
  u = urllib2.urlopen(path)
  tmp_file = open(file_name, 'w')
  tmp_file.write(u.read())
  tmp_file.close()
  return file_name

