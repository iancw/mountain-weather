import pygrib
import datetime
import numpy as np

from model import ParamAndLevel
from model import default_levels, default_level_map


def date_from_rec(grb):
  dt= datetime.strptime("%d%02d" % (grb.dataDate, grb.dataTime), "%Y%m%d%H%M")
  + datetime.timedelta(hours=grb.startStep)
  return dt.replace(tzinfo=utc)

class GribRec:

  def __init__(self, grb):
    self.grb = grb

  def value(self, lat, lon):
    x,y = self.index(lat, lon)
    return self.grb.values[x, y]

  def index(self, lat, lon):
    #lats and lons will have the same shape as data
    lats,lons = self.grb.latlons()
    idx=((lats-lat)**2 + (lons-lon)**2).argmin()
    return np.unravel_index(idx, lats.shape)

class Grib:

  def __init__(self, grb_file):
    self.grb_file = grb_file
    self.grbs = pygrib.open(grb_file)

  def value(self, param_lev, lat, lon):
    self.grbs.seek(0)
    print "Searcing {2} for typeofLevel={0}, shortName={1}".format(param_lev.level, param_lev.shortName, self.grb_file)
    grb = GribRec(self.grbs.select(typeOfLevel=param_lev.level, shortName=param_lev.shortName)[0])
    return grb.value(lat, lon)

  def temperature(self, lat, lon):
    return self.value(default_level_map()['air_temp'], lat, lon)

  def wind_speed(self, lat, lon):
    u = self.value(default_level_map()['wind_u'], lat, lon)
    v = self.value(default_level_map()['wind_v'], lat, lon)
    return np.sqrt(u*u + v*v)

