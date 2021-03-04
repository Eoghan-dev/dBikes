import json
import time
import traceback
from sqlalchemy import create_engine
import requests
import config
import sqlalchemy as sqla
from datetime import datetime

metadata = sqla.MetaData()

# connect to database
engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.DB_USER, config.DB_PASSWORD, config.DB_URL, config.DB_PORT,
                                                   config.DB_NAME))


def store(weather):
    # to do: save weather to database
    print(weather)


# creates the database tables only if missing
metadata.create_all(engine, checkfirst=True)

while True:
    try:
        # get data from JCDecaux url
        r = requests.get(config.OPENWEATHER_URL, params={"appid": config.OPENWEATHER_KEY, "q": "DUBLIN,IE"})
        print("fetching", r.url)
        store(json.loads(r.text))
        print('done')

        # wait 5 min
        time.sleep(5 * 60)

    except:
        print(traceback.format_exc())
