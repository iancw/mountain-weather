from fetch_hrrr import NOAAFetch, HRRR, RAP, NAM
import download
import sub_grib
import os.path
from datetime import *
import urllib2
import pygrib
from record_db import ParamAndLevel
from record_db import default_levels
import re
from grib import Grib

class Hybrid:

  def __init__(self):
    self.hrrr = NOAAFetch(HRRR(), base='../hrrr')
    self.rap = NOAAFetch(RAP(), base='../rap')
    self.nam = NOAAFetch(NAM(), base='../nam')

  def fetch_time(self, dtime):
    '''
    Tries to download a file from HRRR, then falls back to RAP if that fails
    '''
    try:
      return self.hrrr.download_time(dtime)
    except urllib2.HTTPError:
      print "Downloading from HRR failed, trying RAP..."
      try:
        return self.rap.download_time(dtime)
      except urllib2.HTTPError:
        print "Download from RAP failed, trying NAM..."
        return self.nam.download_time(dtime)

# class that abstracts GRIB data
class GribDatabase:
  """Represents GRIB records from online data sources.
  The goal is to make access seamless; if a GRIB is not
  in the local data folder, it will be fetched, sub-sampled,
  and placed into the local database.
  """

  def __init__(self, data_dir, params=default_levels()):
    self.data_dir = data_dir
    self.params = params
    self.date_fmt='%Y_%m_%d_%H%M'
    self.fetcher = Hybrid()

  def leaf_name(self, dt):
    return "{0}.grb2".format(dt.strftime(self.date_fmt))

  def local_path(self, dt):
    return os.path.join(self.data_dir, self.leaf_name(dt))

  def date_for_file(self, fle):
    m = re.search('(\d{4}_\d{2}_\d{2}_\d{2}\d{2})\.', fle)
    return datetime.strptime(m.group(1), self.date_fmt)

  def make_local(self, dt):
    local = self.local_path(dt)
    if not os.path.exists(local):
      print "Local file %s does not exist, attempting to download" % local
      tf = self.fetcher.fetch_time(dt)
      # Create sub-GRIB with only parameters of interest
      local = self.create_sub(tf, dt)
    return local

  def read(self, dtime):
    return Grib(self.make_local(dtime))

  def download_all_hrrr(self):
    """
    Returns the final date_time which was not avaiable as HRRR
    """
    utcnow = datetime.utcnow()
    dt = timedelta(hours=1)
    date_time = datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour)
    # find first working url...
    working = False
    while not working:
      try:
        print "Trying {0}".format(date_time)
        self.make_local(date_time)
        working = True
      except urllib2.HTTPError:
        working = False
        date_time = date_time - dt
    while working:
      try:
        date_time = date_time - dt
        self.make_local(date_time)
      except urllib2.HTTPError:
        working = False
    return date_time


  def create_sub(self, full_grib, dt):
    ''' Extracts a subset of GRIB records from full_grib and
    saves them in a file named the same as full_grib, but in
    the data_dir folder.
    '''
    name, ext = os.path.splitext(full_grib)
    out_file = self.local_path(dt)
    grbout = open(out_file, 'wb')
    print 'creating sub file from ' + full_grib

    grbs = pygrib.open(full_grib)
    for param in self.params:
      print 'finding {0} @ {1}'.format(param.shortName, param.level)
      grbs.seek(0)
      match_grbs = grbs.select(
          shortName=param.shortName,
          typeOfLevel=param.level)
      for grb in match_grbs:
        grbout.write(grb.tostring())
    grbout.close()
    return out_file


