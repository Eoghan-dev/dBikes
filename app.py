from flask import Flask, render_template
#from jinja2 import Template
from sqlalchemy import create_engine
import pandas as pd
import myPrivates

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/about")
def about():
	return app.send_static_file("")

@app.route("/stations")
def stations():
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	df = pd.read_sql_table("stations", engine)
	return df.to_json(orient='records')

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
