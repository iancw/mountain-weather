from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy import desc
from sqlalchemy import and_
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
from model import Location, Measurement, base
from conv import kelv_to_fahr, mps_to_mph, swe_to_in


# for explanation, see http://rehalcon.blogspot.com/2010/03/sqlalchemy-programmingerror-cant-adapt.html
register_adapter(np.float32, lambda x: AsIs(x))



def connect(db_url):
  engine = create_engine(db_url, echo=False)
  return RecordDB(engine)

def create_database(db_url, db_name):
  engine = create_engine(db_url+"postgres", echo=False)
  conn = engine.connect()
  conn.execute("commit")
  conn.execute("create database " + db_name)
  conn.close()


class RecordDB:

  def __init__(self, engine):
    self.engine = engine
    Session = sessionmaker(bind=self.engine)
    self.session = Session()

  def create_tables(self):
    Base = base()
    Base.metadata.create_all(self.engine)
    self.populate_dc_locs()


  def locs(self):
    session = self.make_session()
    return session.query(Location).order_by(Location.id).all()

  def has_record(self, loc, time):
    session = self.make_session()
    meas = session.query(Measurement).filter(and_(Measurement.location_id == loc.id,
      Measurement.date == time))
    return meas.count() > 0

  def add_record(self, measurement):
    session = self.make_session()
    session.add(measurement)
    session.commit()

  def commit(self):
    self.session.commit()

  def close(self):
    self.session.close()

  def add_records(self, measurements):
    session = self.make_session()
    for meas in measurements:
      session.add(meas)
    session.commit()

  def last_record(self):
    ''' Returns datetime of last record
    '''
    session = self.make_session()
    measurements = session.query(Measurement).order_by(desc(Measurement.date)).limit(1)
    if measurements.count() == 0:
      return None
    return measurements[0].date

  def make_session(self):
    return self.session

  def air_temps(self, loc, start, end):
    return self.measurements(loc, lambda m: (m.date, kelv_to_fahr(m.air_temp)), start, end)

  def wind_speed(self, loc, start, end):
    return self.measurements(loc, lambda m: (m.date, mps_to_mph(m.wind_speed)), start, end)

  def snow(self, loc, start, end):
    return self.measurements(loc, lambda m: (m.date, swe_to_in(m.snow)), start, end)

  def measurements(self, loc, param_lambd, start, end):
    session = self.make_session()
    meas = session.query(Measurement).filter(and_(Measurement.location_id == loc.id,
      Measurement.date > start,
      Measurement.date < end)).order_by(Measurement.date)
    pairs = np.array([ param_lambd(m) for m in meas])
    return np.transpose(pairs)

  def populate_dc_locs(self):
    session = self.make_session()
    session.add(Location(name='Overall Falls', lat=38.783360, lon=-78.295143))
    session.add(Location(name='Lewis Spring Falls', lat=38.520638, lon=-78.450539))
    session.add(Location(name='White Oak Canyon', lat=38.555984, lon=-78.353889))
    session.add(Location(name='Finleys Folly', lat=37.911125, lon=-78.973633))
    session.add(Location(name='Hawksbill', lat=38.556441, lon=-78.393894))
    session.add(Location(name='Katahdin', lat=45.9044, lon=-68.8213))
    session.add(Location(name='Mt. Washington', lat=44.2705, lon=-71.3032))
    session.add(Location(name='Gothics', lat=44.128659, lon=-73.857542))
    session.add(Location(name='The Narrows', lat=40.563316, lon=-75.157638))
    session.add(Location(name='White Grass', lat=39.007151, lon=-79.437599))
    session.commit()

