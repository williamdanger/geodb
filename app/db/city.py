import base
from geoalchemy2 import Geography
from sqlalchemy import Column, Date, Integer, String

class City(base.Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    asciiName = Column(String)
    alternateNames = Column(String)
    location = Column(Geography(geometry_type='POINT', srid=4326))
    featureClass = Column(String)
    featureCode = Column(String)
    countryCode = Column(String)
    cc2 = Column(String)
    admin1Code = Column(String)
    admin2Code = Column(String)
    admin3Code = Column(String)
    admin4Code = Column(String)
    population = Column(Integer)
    elevation = Column(Integer)
    dem = Column(String)
    timezone = Column(String)
    modificationDate = Column(Date)
