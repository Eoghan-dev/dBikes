import json
import time
import traceback
from sqlalchemy import create_engine
import requests
import config
import sqlalchemy as sqla

metadata = sqla.MetaData()

# station table
station = sqla.Table('station', metadata,
                     sqla.Column('address', sqla.String(256), nullable=False),
                     sqla.Column('banking', sqla.Integer),
                     sqla.Column('bike_stands', sqla.Integer),
                     sqla.Column('bonus', sqla.Integer),
                     sqla.Column('contract_name', sqla.String(256)),
                     sqla.Column('name', sqla.String(256)),
                     sqla.Column('number', sqla.Integer, unique=True),  # unique numbers
                     sqla.Column('position_lat', sqla.REAL),
                     sqla.Column('position_lng', sqla.REAL),
                     sqla.Column('status', sqla.String(256))
                     )

# availability table
availability = sqla.Table('availability', metadata,
                          sqla.Column('available_bikes', sqla.Integer),
                          sqla.Column('available_bike_stands', sqla.Integer),
                          sqla.Column('number', sqla.Integer),
                          sqla.Column('last_update', sqla.BigInteger) # to do: datetime
                          )


# connect to database
engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.DB_USER, config.DB_PASSWORD, config.DB_URL, config.DB_PORT,
                                                   config.DB_NAME))


def stations_fix_keys(station):
    """move lat and lng in station"""
    station['position_lat'] = station['position']['lat']
    station['position_lng'] = station['position']['lng']
    return station


def store(stations):
    """save station data to database"""
    # add all stations or new stations (ignore duplicate errors)
    engine.execute(station.insert(prefixes=['IGNORE']), *map(stations_fix_keys, stations))
    # add bike availability data
    engine.execute(availability.insert(), *map(stations_fix_keys, stations))


# creates the database tables only if missing
metadata.create_all(engine, checkfirst=True)

while True:
    try:
        # get data from JCDecaux url
        r = requests.get(config.API_URL, params={"apiKey": config.API_KEY, "contract": config.NAME})
        print("fetching", r.url)
        store(json.loads(r.text))
        print('done')

        # wait 5 min
        time.sleep(5 * 60)

    except:
        print(traceback.format_exc())


