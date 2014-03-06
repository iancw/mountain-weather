import record_db
from record_db import Measurement
from grib_db import GribDatabase
import datetime
import os.path
import urllib2
import sys
import matplotlib.pyplot as plt
import numpy as np
import traceback
import os

def db_connect():
  return record_db.connect(os.environ.get('DATABASE_URL'))

def data_folder():
  return os.environ.get('DATA_FOLDER')

class Updater:

  def __init__(self, db, gribs):
    self.db = db
    self.gribs = gribs
    self.locs = self.db.locs()


  def fetch_data_between(self, start, end):
    delta = datetime.timedelta(hours=1)
    cur = start.replace(minute=0, second=0, microsecond=0)
    while cur < end:
      try:
        self.add_record(cur)
        self.db.commit()
      except (urllib2.HTTPError):
        print "failed to download %s: %s" % (cur.strftime("%Y-%m-%d-%H%M"),  sys.exc_info())
        traceback.print_exc()
      except (ValueError):
        traceback.print_exc()
      cur = cur + delta


  def add_record(self, dtime):
    for loc in self.locs:
      if self.db.has_record(loc, dtime):
        #print "Record at {0}, {1} already present, skipping".format(loc.name, dtime)
        pass
      else:
        self.db.add_record(self.build_meas(dtime, loc))

  def build_meas(self, dtime, loc):
    print "Building measurement for %s at %s" % (dtime.strftime('%Y-%m-%d-%H%M'), loc.name)
    grb = self.gribs.read(dtime)
    return Measurement(date=dtime,
        air_temp=grb.temperature(loc.lat, loc.lon),
        wind_speed=grb.wind_speed(loc.lat, loc.lon),
        snow=grb.snow(loc.lat, loc.lon),
        location_id=loc.id)

def up_to_now():
  now = datetime.datetime.utcnow()
  season_start = now - datetime.timedelta(days=7)
  ensure_data_between(season_start, now)

def ensure_data_between(s, e):
  db = db_connect()
  gribs = GribDatabase(data_folder())
  u = Updater(db, gribs)
  u.fetch_data_between(s, e)

def hour_diff(frm, to):
  td = to - frm
  return td.days * 24.0 + td.seconds / 3600.0

def plot_temp(db, loc, s, e):
  ensure_data_between(s, e)
  dates, temps = db.air_temps(loc, s, e)
  temps = (temps - 273.15) * 1.8 + 32
  date_offsets = np.array([ hour_diff(s, d) for d in dates])
  plt.plot(dates, temps)

def query_temps():
  db = db_connect()
  kat = db.locs()[-2]
  s = datetime.datetime(2014, 1, 1, 0)
  e = datetime.datetime(2014, 1, 11, 0)
  plot_temp(db, kat, s, e)

  plt.title("Temperature (F) at {0}".format(kat.name))
  plt.show()

if __name__ == '__main__':
  #query_temps()
  up_to_now()

