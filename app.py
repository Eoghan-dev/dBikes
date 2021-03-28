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

@app.route("/dropdown")
def dropdown():
    return app.send_static_file("dropdown.html")

@app.route("/stations")
def stations():
	engine = create_engine(f"mysql+mysqlconnector://{myPrivates.user}:{myPrivates.dbPass}@{myPrivates.dbURL}:{myPrivates.port}/{myPrivates.dbName}")
	df = pd.read_sql_table("stations", engine)
	return df.to_json(orient='records')

if __name__ == "__main__":
	app.run(debug=True)
