from flask import Flask, render_template
#from jinja2 import Template
from sqlalchemy import create_engine
import pandas as pd
import pickle
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
