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

  def up_to_now(self):
    last = self.db.last_record()
    if last is None:
      last = datetime.datetime(2014, 1, 4, 16)
    print "starting from {0}".format(last)
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(hours=1)
    cur = last + delta
    while cur < now:
      try:
        self.add_record(cur)
        self.db.commit()
      except (urllib2.HTTPError, ValueError):
        print "failed to download %s: %s" % (cur.strftime("%Y-%m-%d-%H%M"),  sys.exc_info()[0])
      cur = cur + delta

  def add_record(self, dtime):
    for loc in self.locs:
      self.db.add_record(self.build_meas(dtime, loc))

  def build_meas(self, dtime, loc):
    print "Building measurement for %s at %s" % (dtime.strftime('%Y-%m-%d-%H%M'), loc.name)
    grb = self.gribs.read(dtime)
    return Measurement(date=dtime,
        air_temp=grb.temperature(loc.lat, loc.lon),
        wind_speed=grb.wind_speed(loc.lat, loc.lon),
        location_id=loc.id)

def run_up_to_now():
  need_init = False
  if not os.path.exists('test.db'):
    need_init = True
  db = record_db.connect("sqlite:///test.db")
  if need_init:
    record_db.init_database(db)
  gribs = GribDatabase('./data/')
  u = Updater(db, gribs)
  u.up_to_now()

def query_temps():
  run_up_to_now()
  db = record_db.connect("sqlite:///test.db")
  s = datetime.datetime(2013, 3, 15, 0)
  e = datetime.datetime(2013, 3, 31, 0)
  kat = db.locs()[-2]
  time_ser = db.air_temps(kat, s, e)
  dates, temps = np.transpose(time_ser)
  temps = (temps - 273.15) * 1.8 + 32
  plt.plot(dates, temps)
  plt.title("Temperature (F) at {0}".format(kat.name))
  plt.show()

if __name__ == '__main__':
  query_temps()

