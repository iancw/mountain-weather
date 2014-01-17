from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import desc
from sqlalchemy import and_
import numpy as np

Base = declarative_base()

def kelv_to_fahr(k):
  return ((k - 273.15) * 1.8) + 32.0

def mps_to_mph(ms):
  return 2.23694 * ms

class Location(Base):
  __tablename__ = "location"

  id = Column(Integer, primary_key=True)
  name = Column(String, unique=True)
  lat = Column(Float)
  lon = Column(Float)

  def __repr__(self):
    return "<Location(name='%s', lat=%f, lon=%f)>" % (self.name, self.lat, self.lon)

class Measurement(Base):
  __tablename__ = 'measurement'
  __table_args__ = (UniqueConstraint('date', 'location_id', name='_date_loc_uc'),)

  id = Column(Integer, primary_key=True)
  date = Column(DateTime)
  air_temp = Column(Float)
  wind_speed = Column(Float)
  location_id = Column(Integer, ForeignKey('location.id'))

  location = relationship("Location", backref=backref('measurements', order_by=date))

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
      #ParamAndLevel('gust', 'Wind Gust', 'surface'),
      #ParamAndLevel('sdwe', 'Snow Depth', 'surface'),
      ParamAndLevel('10u', 'Wind Speed U', 'heightAboveGround'),
      ParamAndLevel('10v', 'Wind Speed V', 'heightAboveGround')]

def default_level_map():
  return {'air_temp': ParamAndLevel('t', 'Temperature', 'surface'),
  'precip': ParamAndLevel('acpcp', 'Convective precip', 'surface'),
  #'wind_gust': ParamAndLevel('gust', 'Wind Gust', 'surface'),
  #'snow_depth': ParamAndLevel('sdwe', 'Snow Depth', 'surface'),
  'wind_u':  ParamAndLevel('10u', 'Wind Speed U', 'heightAboveGround'),
  'wind_v':  ParamAndLevel('10v', 'Wind Speed V', 'heightAboveGround')}

def connect(db_url):
  engine = create_engine(db_url, echo=False)
  return RecordDB(engine)

def create_database(db_url, db_name):
  engine = create_engine(db_url+"postgres", echo=False)
  conn = engine.connect()
  conn.execute("commit")
  conn.execute("create database " + db_name)
  conn.close()

def init_database(rec_db):
  Base.metadata.create_all(rec_db.engine)
  rec_db.populate_dc_locs()

class RecordDB:

  def __init__(self, engine):
    self.engine = engine
    Session = sessionmaker(bind=self.engine)
    self.session = Session()

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
    Session = sessionmaker(bind=self.engine)
    return Session()

  def air_temps(self, loc, start, end):
    return self.measurements(loc, lambda m: (m.date, kelv_to_fahr(m.air_temp)), start, end)

  def wind_speed(self, loc, start, end):
    return self.measurements(loc, lambda m: (m.date, mps_to_mph(m.wind_speed)), start, end)

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
    session.add(Location(name='Hawksbill', lat=38.596, lon=-78.259)) # Grid cell 470,227
    session.add(Location(name='Katahdin', lat=45.9044, lon=-68.8213))
    session.add(Location(name='Mt. Washington', lat=44.2705, lon=-71.3032))
    session.add(Location(name='Gothics', lat=44.128659, lon=-73.857542))
    session.add(Location(name='The Narrows', lat=40.563316, lon=-75.157638))
    session.add(Location(name='White Grass', lat=39.007151, lon=-79.437599))
    session.commit()

