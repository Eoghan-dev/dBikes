from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd
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
	query = f"""SELECT number, last_update, available_bikes, available_bike_stands FROM dbikes.availability 
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
	query = f"""SELECT number, dayname(last_update), avg(available_bikes), avg(available_bike_stands) FROM dbikes.availability 
	WHERE number = {station_id} GROUP BY dayname(last_update)"""

	df = pd.read_sql_query(query, engine)
	df_result = df.set_index('dayname(last_update)')
	df_result['last_update_day'] = df_result.index
	df_result.rename(columns={"avg(available_bikes)": "available_bikes"}, inplace=True)

	return df_result.to_json(orient='records')

@app.route("/weather")
def weather():
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	# read current weather from database
	df = pd.read_sql_table("current_weather", engine)
	# sort by date descending
	df = df.sort_values(by='dt', ascending=False)
	# get first row
	value = df.head(1)
	# return weather as json
	return value.to_json(orient="records")

if __name__ == "__main__":
	app.run(debug=True)
