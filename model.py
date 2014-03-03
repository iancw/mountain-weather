from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

def base():
  return Base

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
  precip = Column(Float)
  location_id = Column(Integer, ForeignKey('location.id'))

  location = relationship("Location", backref=backref('measurements', order_by=date))

class ParamAndLevel:
  def __init__(self, shortName, fullName, level):
    self.shortName = shortName
    self.fullName = fullName
    self.level = level

