import json
import time
import traceback
from sqlalchemy import create_engine, Table, Column, DateTime, Integer, Float, String
import requests
import config
import sqlalchemy as sqla
from datetime import datetime

metadata = sqla.MetaData()

# connect to database
engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.DB_USER, config.DB_PASSWORD, config.DB_URL, config.DB_PORT,
                                                   config.DB_NAME))

# current weather
current = Table('current_weather', metadata,
                Column("dt", DateTime, primary_key=True),
                Column("sunrise", DateTime),
                Column("sunset", DateTime),
                Column("temp", Float),
                Column("feels_like", Float),
                Column("pressure", Integer),
                Column("humidity", Integer),
                Column("dew_point", Float),
                Column("uvi", Float),
                Column("clouds", Integer),
                Column("visibility", Integer),
                Column("wind_speed", Float),
                Column("wind_deg", Float),
                Column("weather_id", Integer),
                Column("weather_main", String(100)),
                Column("weather_description", String(200)),
                Column("weather_icon", String(10)))

# daily weather
daily = Table('daily_weather', metadata,
              Column("dt", DateTime, primary_key=True),
              Column("future_dt", DateTime, primary_key=True),
              Column("sunrise", DateTime),
              Column("sunset", DateTime),
              Column("temp_day", Float),
              Column("temp_min", Float),
              Column("temp_max", Float),
              Column("temp_night", Float),
              Column("temp_eve", Float),
              Column("temp_morn", Float),
              Column("feels_like_day", Float),
              Column("feels_like_night", Float),
              Column("feels_like_eve", Float),
              Column("feels_like_morn", Float),
              Column("pressure", Integer),
              Column("humidity", Integer),
              Column("dew_point", Float),
              Column("wind_speed", Float),
              Column("wind_deg", Float),
              Column("weather_id", Integer),
              Column("weather_main", String(100)),
              Column("weather_description", String(200)),
              Column("weather_icon", String(10)),
              Column("clouds", Integer),
              Column("pop", Float),
              Column("uvi", Float))

# hourly weather
hourly = Table('hourly_weather', metadata,
               Column("dt", DateTime, primary_key=True),
               Column("future_dt", DateTime, primary_key=True),
               Column("temp", Float),
               Column("feels_like", Float),
               Column("pressure", Integer),
               Column("humidity", Integer),
               Column("dew_point", Float),
               Column("uvi", Float),
               Column("clouds", Integer),
               Column("visibility", Integer),
               Column("wind_speed", Float),
               Column("wind_deg", Float),
               Column("weather_id", Integer),
               Column("weather_main", String(100)),
               Column("weather_description", String(200)),
               Column("weather_icon", String(10)),
               Column("pop", Float))


def store(weather):
    # to do: save weather to database
    print(weather)


# creates the database tables only if missing
metadata.create_all(engine, checkfirst=True)

while True:
    try:
        # get the data from openweather
        data = {
            "appid": config.OPENWEATHER_KEY,
            "lat": 53.344,
            "lon": -6.2672,
            "exclude": "minutely"
        }
        r = requests.get(config.OPENWEATHER_URL, params=data)
        print("fetching", r.url)
        store(json.loads(r.text))
        print('done')

        # wait 30 min
        time.sleep(30 * 60)

    except:
        print(traceback.format_exc())
