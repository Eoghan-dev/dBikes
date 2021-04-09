import datetime
import json

from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd
import pickle
import myPrivates
from functools import lru_cache

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/about")
def about():
	return app.send_static_file("")

@app.route("/stations")
@lru_cache
def stations():
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	df = pd.read_sql_table("stations", engine)
	return df.to_json(orient='records')

@app.route("/occupancyD/<int:station_id>")
@lru_cache
def get_occupancyDay(station_id):
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	#experiment with query in jupyter notebook
	query = f"""SELECT number, last_update, available_bikes, available_bike_stands FROM availability 
	WHERE number = {station_id}"""

	df = pd.read_sql_query(query, engine)
	df_result = df.set_index('last_update').resample('1d').mean()
	df_result['last_update'] = df_result.index

	return df_result.to_json(orient='records')

@app.route("/occupancyW/<int:station_id>")
@lru_cache
def get_occupancyWeek(station_id):
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	#experiment with query in jupyter notebook
	query = f"""SELECT number, dayname(last_update), avg(available_bikes), avg(available_bike_stands) FROM availability 
	WHERE number = {station_id} GROUP BY dayname(last_update)"""

	df = pd.read_sql_query(query, engine)
	df_result = df.set_index('dayname(last_update)')
	df_result['last_update_day'] = df_result.index
	df_result.rename(columns={"avg(available_bikes)": "available_bikes"}, inplace=True)

	return df_result.to_json(orient='records')

@app.route("/weather")
def current_weather():
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	# read current weather from database
	df = pd.read_sql_table("current_weather", engine)
	# sort by date descending
	df = df.sort_values(by='dt', ascending=False)
	# get first row
	value = df.head(1)
	# return weather as json
	return value.to_json(orient="records")

@app.route("/weather/<int:req_day>/<int:req_time>")
def weather_forecast(req_day, req_time):
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	# get today as weekday
	today = datetime.datetime.today().weekday()
	# get current hour
	hour = datetime.datetime.today().hour
	# calculate the correct date for the requested weekday
	date = datetime.datetime.today() + datetime.timedelta(req_day - today)
	# check if the date is in the past
	if today == req_day and req_time <= hour:
		return {}
	# transform the date to 'yyyy-mm-dd HH:MM'
	future_dt = date.strftime('%Y-%m-%d') + ' ' + str(req_time) + ':00'
	# get weather forecast from hourly weather table
	sql = f"SELECT * FROM hourly_weather WHERE future_dt='{future_dt}' ORDER BY dt DESC LIMIT 1"
	weather_df = pd.read_sql_query(sql, engine)
	if weather_df.empty:
		# if no forecast return empty
		return {}
	else:
		return weather_df.to_json(orient="records")

def predict(station_number, temp=281.11, humidity=60, wind_speed=0, weather_id=803, week_day=0, hour=12):
    """ Predict available bikes for station, weekday, hour, and weather. """
    # prepare features
    data = {
        'temp': [temp],
        'humidity': [humidity],
        'wind_speed': [wind_speed],
        'weather_id': [weather_id],
        'weekday': [week_day],
        'hour': [hour]
    }

    # create dataframe
    X = pd.DataFrame.from_dict(data)

    # load model from file
    with open('models/' + str(station_number) + '.pkl', 'rb') as file:
        model = pickle.load(file)

    # get prediction from model
    y = model.predict(X)

    # return the prediction
    return int(round(y[0]))

if __name__ == "__main__":
	app.run(debug=True)
