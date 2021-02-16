name = "Dublin"
stations = "https://api.jcdecaux.com/vls/v1/stations"
apikey = "940341f15a8989421a09f44a2e4527427f4c95dd"


#run all the time
while True:
	try:
		r = requests.get(stations,params={"apikey"=apikey, "contract"=name})
		store(json.loads(r.text))

		#sleep for 5 minutes
	except:
		print(traceback.format_exc())

