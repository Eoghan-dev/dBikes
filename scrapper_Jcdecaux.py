'''
Import all modules needed to request the data and convert to the 
table format needed to store on rds database.

myPrivates.py should contain sensitive information 
required to access the API and rds database.
'''
import myPrivates
import requests
import json
import traceback
import datetime
import salalchemy.dialects
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, DateTime

'''
Below variables used in f strings are declared. These
variables specifically the priavte ones are defined here
for ease of reading while constructing strings
'''
name = "dublin"
stations_API = "https://api.jcdecaux.com/vls/v1/stations"
apikey = myPrivates.myKey
dbPass = myPrivates.dbPass
db_url = myPrivates.dbURL
user = "admin"
dbName = "dbikes"
sqlport = "3306"

'''
Create sql engine here as to not recreate every time data
is sent to the rds database
'''
engine = create_engine(f"mysql+mysqlconnector://{user}:{dbPass}@{db_url}:{sqlport}/{dbName}")

#run all the time
while True:
	try:
		r = requests.get(stations,params={"apiKey":apikey, "contract":name})
		values = list(map(get_station,r.json()))
		send2mysql(engine,values)

		#sleep for 5 minutes
	except:
		print(traceback.format_exc())



def get_station(obj):
	#make list of dicts from json
	pass

def send2mysql():
	#send to rds database
	pass
