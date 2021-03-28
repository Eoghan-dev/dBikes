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

@app.route("/occupancy/<int:station_id>")
@lru_cache
def get_occupancy(station_id):
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	#experiment with query in jupyter notebook
	query = f"""SELECT number, last_update, available_bikes, available_bike_stands FROM dbikes.availability 
	WHERE number = {station_id}"""

	df = pd.read_sql_query(query, engine)
	df_result = df.set_index('last_update').resample('1d').mean()
	df_result['last_update'] = df_result.index

	#df_result.to_json(orient='records') this returns string pair with json.loads()?

	return df_result.to_json(orient='records')

if __name__ == "__main__":
	app.run(debug=True)
