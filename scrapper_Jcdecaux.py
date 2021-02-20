#myPrivates should be a python file containing you key for jcdecaux
from myPrivates import myKey

name = "dublin"
stations = "https://api.jcdecaux.com/vls/v1/stations"
apikey = myKey


#run all the time
#some changes need to be made for sql connection

def main():
	while True:
		try:
			r = requests.get(stations,params={"apiKey":apikey, "contract":name})
			store(json.loads(r.text))

			#sleep for 5 minutes
		except:
			print(traceback.format_exc())



	def w2panda_db():
		#write json request to panda db
		pass

	def send2aws():
		#send data to aws database
		pass
