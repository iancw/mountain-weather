from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Location(Base):
  __tablename__ = "location"

  id = Column(Integer, primary_key=True)
  name = Column(String)
  lat = Column(Float)
  lon = Column(Float)

  def __repr__(self):
    return "<Location(name='%s', lat=%f, lon=%f)>" % (self.name, self.lat, self.lon)

class Measurement(Base):
  __tablename__ = 'measurement'

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
      ParamAndLevel('gust', 'Wind Gust', 'surface'),
      ParamAndLevel('sdwe', 'Snow Depth', 'surface'),
      ParamAndLevel('10u', 'Wind Speed U', 'heightAboveGround'),
      ParamAndLevel('10v', 'Wind Speed V', 'heightAboveGround')]

def default_level_map():
  return {'air_temp': ParamAndLevel('t', 'Temperature', 'surface'),
  'precip': ParamAndLevel('acpcp', 'Convective precip', 'surface'),
  'wind_gust': ParamAndLevel('gust', 'Wind Gust', 'surface'),
  'snow_depth': ParamAndLevel('sdwe', 'Snow Depth', 'surface'),
  'wind_u':  ParamAndLevel('10u', 'Wind Speed U', 'heightAboveGround'),
  'wind_v':  ParamAndLevel('10v', 'Wind Speed V', 'heightAboveGround')}


def connect(db_url):
  engine = create_engine(db_url, echo=False)
  return RecordDB(engine)

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
    return session.query(Location).order_by(Location.id)

  def add_record(self, measurement):
    session = self.make_session()
    session.add(measurement)
    session.commit()

  def commit(self):
    self.session.commit()

  def add_records(self, measurements):
    session = self.make_session()
    for meas in measurements:
      session.add(meas)
    session.commit()

  def last_record(self):
    ''' Returns datetime of last record
    '''
    session = self.make_session()
    measurements = session.query(Measurement).order_by(Measurement.date)
    print "QUERY RETURNED:  ", measurements
    print "COUNT IS ", measurements.count()
    print "END QUERY"
    if measurements.count() == 0:
      return None
    print "FIRST: ", measurements[0].date
    print "LAST: ", measurements[-1].date
    return measurements[-1].date

  def make_session(self):
    Session = sessionmaker(bind=self.engine)
    return Session()

  def get_records(self, loc, param, start, end):
    session = self.make_session()
    return session.query(Measurement)

  def populate_dc_locs(self):
    session = self.make_session()
    session.add(Location(name='Overall Falls', lat=38.783360, lon=-78.295143))
    session.add(Location(name='Lewis Spring Falls', lat=38.520638, lon=-78.450539))
    session.add(Location(name='White oak canyon', lat=38.555984, lon=-78.353889))
    session.add(Location(name='Finleys Folly', lat=37.911125, lon=-78.973633))
    session.add(Location(name='Hawksbill', lat=38.596, lon=-78.259)) # Grid cell 470,227
    session.add(Location(name='Katahdin', lat=45.9044, lon=-68.8213))
    session.add(Location(name='Mt. Washington', lat=44.2705, lon=-71.3032))
    session.commit()

