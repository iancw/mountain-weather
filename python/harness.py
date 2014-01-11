import record_db
from record_db import Measurement
from data_abs import GribDatabase
import datetime
import os.path
import urllib2
import sys
import matplotlib.pyplot as plt
import numpy as np

class Updater:

  def __init__(self, db, gribs):
    self.db = db
    self.gribs = gribs
    self.locs = self.db.locs()


  def fetch_data_between(self, start, end):
    delta = datetime.timedelta(hours=1)
    cur = start
    while cur < end:
      try:
        self.add_record(cur)
        self.db.commit()
      except (urllib2.HTTPError, ValueError):
        print "failed to download %s: %s" % (cur.strftime("%Y-%m-%d-%H%M"),  sys.exc_info()[0])
      cur = cur + delta


  def add_record(self, dtime):
    for loc in self.locs:
      if self.db.has_record(loc, dtime):
        print "Record at {0}, {1} already present, skipping".format(loc.name, dtime)
      else:
        self.db.add_record(self.build_meas(dtime, loc))

  def build_meas(self, dtime, loc):
    print "Building measurement for %s at %s" % (dtime.strftime('%Y-%m-%d-%H%M'), loc.name)
    grb = self.gribs.read(dtime)
    return Measurement(date=dtime,
        air_temp=grb.temperature(loc.lat, loc.lon),
        wind_speed=grb.wind_speed(loc.lat, loc.lon),
        location_id=loc.id)

def up_to_now(self):
  season_start = datetime.datetime(2014, 1, 4, 16)
  now = datetime.datetime.utcnow()
  ensure_dta_between(season_start, now)

def ensure_data_between(s, e):
  need_init = False
  if not os.path.exists('test.db'):
    need_init = True
  db = record_db.connect("sqlite:///test.db")
  if need_init:
    record_db.init_database(db)
  gribs = GribDatabase('../data/')
  u = Updater(db, gribs)
  u.fetch_data_between(s, e)


def query_temps():
  db = record_db.connect("sqlite:///test.db")
  s = datetime.datetime(2013, 3, 15, 0)
  e = datetime.datetime(2013, 3, 31, 0)
  ensure_data_between(s, e)
  kat = db.locs()[-2]
  time_ser = db.air_temps(kat, s, e)
  dates, temps = np.transpose(time_ser)
  temps = (temps - 273.15) * 1.8 + 32
  plt.plot(dates, temps)
  plt.title("Temperature (F) at {0}".format(kat.name))
  plt.show()

if __name__ == '__main__':
  query_temps()

