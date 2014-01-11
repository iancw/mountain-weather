import os
import os.path
import urllib2
from datetime import *

def yrmoday(dt):
  return dt.strftime('%Y%m%d')

def yrmo(dt):
  return dt.strftime('%Y%m')

class HRRR:

  def __init__(self):
    self.root = 'http://hrrr.agron.iastate.edu/data/hrrr'

  def time_format(self, dt):
    return dt.strftime('%Y%m%d%H%M')

  # e.g. 201312031000/
  # followed by...
  # hrrr.2d.201312270500f000.grib2
  # hrrr.2d.201312270500f001.grib2
  # hrrr.2d.2013 12 27 05 00 f001.grib2
  # suffixes include f000 through f011
  def leaf_file(self, dt):
    return 'hrrr.2d.{0}f000.grib2'.format(self.time_format(dt))

  def sub_path(self, dt):
    return '{0}/{1}'.format(self.time_format(dt), self.leaf_file(dt))

  def build_path(self, dt):
    return '{0}/{1}'.format(self.root(), self.sub_path(dt))


class RAP:

  def __init__(self):
    self.root='http://nomads.ncdc.noaa.gov/data/rap130'

  # e.g. http://nomads.ncdc.noaa.gov/data/rap130/201303/20130323/rap_130_20130323_2300_018.grb2
  def build_path(self, dt):
    ''' Returns the full URL to the remote resource '''
    return '{0}/{1}/{2}'.format(self.root, self.sub_path(dt), self.leaf_file(dt))

  # e.g. 201303/20130323
  def sub_path(self, dt):
    return '{0}/{1}'.format(yrmo(dt), yrmoday(dt))

  def leaf_file(self, dt):
    return self.leaf_file(dt, 0, 0)

  # E.g. rap_130_20130323_2300_018.grb2
  def leaf_file(self, dt, base, tau):
    ''' Returns a local filename for the given time'''
    daymoyr = dt.strftime('%Y%m%d')
    return 'rap_130_{1}_{2}_{3}.grb2'.format(daymoyr, '%02d00' % base, '%03d' % tau)

class NOAAFetch:

  def __init__(self, path_builder):
    self.path_builder = path_builder

  def download_time(self, dt):
    path=self.path_builder.build_path(dt)
    file_name = self.path_builder.leaf_file(dt)
    if os.path.exists(os.path.join('.', file_name)):
      print "File {0} already present, returning".format(path)
      return file_name
    print "Downloading {0}".format(path)
    u = urllib2.urlopen(path)
    tmp_file = open(file_name, 'w')
    tmp_file.write(u.read())
    tmp_file.close()
    return file_name

