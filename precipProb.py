# users can edit serialJSONFunction.py to replace soil moisture with precipitation probability from DarkSky
import requests
import json 
import statistics

# edit the API call with your DarkSky API Key and coordinates 

def getProbeMoisture():
	try:
		# pass  DarkSky API Key and lat/lon for a  weather prediction
		r = requests.get('https://api.darksky.net/forecast/<yourDarkSkyKey>/40.816349,-73.939728')
		data = r.json()
		#current = data["currently"]
		hourly = data["hourly"]["data"]

		dayOneSample = []
		dayTwoSample  = []
		# 49 results - for 2 day forecast 
		# parse  data - since it is every hour, the current time will be between  0 and 1 
		for i in range(0,len(hourly)):
			if i < 25:
				dayOneSample.append(hourly[i]['precipProbability'])
			if i >= 25:
				dayTwoSample.append(hourly[i]['precipProbability'])

		dayOneAvg = statistics.mean(dayOneSample)
		dayTwoAvg = statistics.mean(dayTwoSample)
	except:
		# make it one percent if api call errors 
		dayOneAvg = 0.001
		dayTwoAvg = 0.001
		
	
	global vwc6Avg
	
	try:
		vwc6Avg = round((100*dayOneAvg),4)
		print("24 hr avg precipitation probability "+str(vwc6Avg))
	except:
		# make sure to initialize serial.json  w a value: {"moisture": 30}
		with open('serial.json') as json_file:
			vwc6Avg = json.load(json_file)
			vwc6Avg = vwc6Avg["moisture"]
		print("precipProb call not succesful")
	
	global moistureSample
	moistureSample = {'moisture': vwc6Avg}
