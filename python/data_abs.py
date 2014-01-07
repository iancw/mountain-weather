import fetch_hrrr
import download
import sub_grib
import os.path
from datetime import *
import urllib2
import pygrib
# class that abstracts GRIB data

class ParamAndLevel:
  def __init__(self, shortName, fullName, level):
    self.shortName = shortName
    self.fullName = fullName
    self.level = level

def default_levels():
  #surface_names=['t', 'acpcp', 'gust', 'sdwe']
  #agl_names=['10u', '10v']
  return [ParamAndLevel('t', 'Temperature', 'surface'),
      ParamAndLevel('acpcp', 'Convective precip', 'surface'),
      ParamAndLevel('gust', 'Wind Gust', 'surface'),
      ParamAndLevel('sdwe', 'Snow Depth', 'surface'),
      ParamAndLevel('10u', 'Wind Speed U', 'heightAboveGround'),
      ParamAndLevel('10v', 'Wind Speed V', 'heightAboveGround')]

class GribDatabase:
  """Represents GRIB records from online data sources.
  The goal is to make access seamless; if a GRIB is not
  in the local data folder, it will be fetched, sub-sampled,
  and placed into the local database.
  """

  def __init__(self, data_dir, params=default_levels(), season_start=datetime(2013, 11, 1)):
    self.data_dir = data_dir
    self.params = params
    self.season_start = season_start

  def local_hrrr_name(self, dt):
    return "hrrr_{0}.grb2".format(dt.strftime('%Y_%m_%d_%H%M'))

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
        self.fetch_and_process_hrrr(date_time)
        working = True
      except urllib2.HTTPError:
        working = False
        date_time = date_time - dt
    while working:
      try:
        date_time = date_time - dt
        self.fetch_and_process_hrrr(date_time)
      except urllib2.HTTPError:
        working = False
    return date_time

  def local_filename(self, dt):
    return os.path.join(self.data_dir, self.local_hrrr_name(dt))

  def create_sub(self, full_grib, dt):
    ''' Extracts a subset of GRIB records from full_grib and
    saves them in a file named the same as full_grib, but in
    the data_dir folder.
    '''
    name, ext = os.path.splitext(full_grib)
    out_file = self.local_filename(dt)
    grbout = open(out_file, 'wb')

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

  def fetch_and_process_hrrr(self, dt):
    local = self.local_filename(dt)
    if not os.path.exists(local):
      tf = fetch_hrrr.download_time(dt)
      # Create sub-GRIB with only parameters of interest
      local = self.create_sub(tf, dt)
    return local

