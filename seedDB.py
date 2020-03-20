import os
import psycopg2
import sqlalchemy

from datetime import datetime
from app.db import city
from sqlalchemy.orm import sessionmaker
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Setup the database with a user that can enable PostGIS
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
cursor.execute('CREATE USER geouser WITH superuser')
cursor.execute('CREATE DATABASE geodb')
cursor.execute('GRANT ALL PRIVILEGES ON DATABASE geodb TO geouser')
cursor.close()
conn.close()

# Actually enable PostGIS
engine = sqlalchemy.create_engine(os.getenv('DATABASE_URL'), echo=True)
with engine.connect() as conn:
    conn.execute('CREATE EXTENSION postgis')

with engine.connect() as conn:
    city.City.__table__.create(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open('./data/cities1000.csv', 'rb') as f:
        count = 0
        for cityData in f.readlines():
            cityFields = cityData.split('\t')
            newCity = city.City(
                id=cityFields[0],
                name=cityFields[1],
                asciiName=cityFields[2],
                alternateNames=cityFields[3],
                location='POINT(%s %s)' % (cityFields[4], cityFields[5]),
                featureClass=cityFields[6],
                featureCode=cityFields[7],
                countryCode=cityFields[8],
                cc2=cityFields[9],
                admin1Code=cityFields[10],
                admin2Code=cityFields[11],
                admin3Code=cityFields[12],
                admin4Code=cityFields[13],
                population=cityFields[14] or None,
                elevation=cityFields[15] or None,
                dem=cityFields[16],
                timezone=cityFields[17],
                modificationDate=datetime.strptime(cityFields[18].strip(), '%Y-%m-%d'),
            )
            session.add(newCity)
            count += 1
            if not count % 10000:
                print 'Added %s cities so far' % count

        session.commit()

print 'Seeding complete.  Locate some cities!'
