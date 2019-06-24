import requests, json
from datetime import datetime, timezone, timedelta
import statistics
import time

#irrigiationController configuration
controller = requests.get('http://app.plantgroup.co/api/controllers/Teralytic-1/config')
controllerParams = controller.json()
print("RainBox Irrigation Parameters")
print(controllerParams)

wateringScheduleList = controllerParams['config']['user']['watering_schedule']
#print(wateringScheduleList)
waterSchedListLen = len(wateringScheduleList)

#if multiple times are set in the controller, append this empty list
irrigationSchedule = []

#boolean for whether or not irrigation is currently on
irrigationOn = False
# condition for whether current Time is within irrigation timer window and should check for vwc
checkMoistureHour = False
checkMoistureMinute = False

if waterSchedListLen == 1:
        irrigationTime = wateringScheduleList[0]
        print(irrigationTime)
        irrigationStartTime = irrigationTime['begin']
        #print(type(irrigationStartTime))
        # split the string by :
        irrigationStartTime = irrigationStartTime.split(':')
        irrigationStartHour = irrigationStartTime[0]
        irrigationStartMinute = irrigationStartTime[1]
        print("Irrigation Start Time: " + str(irrigationStartHour)+":"+str(irrigationStartMinute))
        # deal with 2 digit formatting for hour and minute leading zero
        #print(len(irrigationStartHour))
        #print(len(irrigationStartMinute))
        if len(irrigationStartHour) == 2 and int(irrigationStartHour[0]) == 0:
                irrigationStartHour = int(irrigationStartHour[1])
        else:
                irrigationStartHour = int(irrigationStartHour)
        #print(irrigationStartHour)

        if len(irrigationStartMinute) == 2 and int(irrigationStartMinute[0]) == 0:
                irrigationStartMinute  = int(irrigationStartMinute[1])
        else:
                irrigationStartMinute = int(irrigationStartMinute)
        #print(irrigationStartMinute)

        #end Time
        irrigationEndTime = irrigationTime['end']
        irrigationEndTime = irrigationEndTime.split(":")
        irrigationEndHour = irrigationEndTime[0]
        irrigationEndMinute = irrigationEndTime[1]
        print("Irrigation End Time: " + str(irrigationEndHour)+":"+str(irrigationEndMinute))
        if len(irrigationEndHour) == 2 and int(irrigationEndHour[0]) == 0:
                irrigationEndHour = int(irrigationEndHour[1])
        else:
                irrigationEndHour = int(irrigationEndHour)
        if len(irrigationEndMinute) == 2 and int(irrigationEndMinute[0]) == 0:
                irrigationEndMinute = int(irrigationEndMinute[1])
        else:
                irrigationEndMinute = int(irrigationEndMinute)
        #local time from the Pi
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        #print("Current Time: ")
        #print(now)
        print("Current Hour: " + str(hour))
        print("Current Minute: " + str(minute))
        if hour >= irrigationStartHour and hour <= irrigationEndHour:        
                checkMoistureHour = True

        if checkMoistureHour == True:
                print("Within allowable irrigation time window, searching for moisture data...")
        
        #soil moisture threshold
        moistureThresh = controllerParams['config']['user']['soil_moisture_threshold']
        moistureThresh = int(moistureThresh)
        print("Soil Mosture Threshold: " + str(moistureThresh))
        
elif waterSchedListLen > 1:
        for i in waterScheduleList:
                #print(i)
                irrigationSchedule.append(i)
                print("Multiple irrrigation time windows saved")
                print(irrigationSchedule)
else:
        print("No irrigation timer presets passed in.")
        
# sample soil moisture sensor data 

#teralytic sensor & API configuration
token_url = "https://auth.teralytic.io/token"
client_id = 'xxxx'
client_secret = 'xxx'
# soil API call
apiKey = 'xxx'

#step A, B - single call with client credentials as the basic auth header - will return access_token
data = {'grant_type': 'client_credentials'}

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

tokens = json.loads(access_token_response.text)

#print(tokens)

accessToken = tokens['access_token']
#print(accessToken)

#TIME FORMAT
#startTime  = '2019-02-27 13:39:54.185243'
#endTime = '2019-02-27 14:39:54.185187'

#start in the past
startTime = datetime.now() - timedelta(hours = 24)
#print("Time Window:")
print("-------------")
#print("Start Time: " + str(startTime))
# end in the present
endTime = datetime.now()
#print("End Time: " + str(endTime))
startYear = startTime.year
startMonth = f"{startTime:%m}"
startDay = f"{startTime:%d}"
startHour = f"{startTime.hour:02d}" 
startMinute  = f"{startTime.minute:02d}" 
startSecond = f"{startTime.second:02d}"
######
########
endYear = endTime.year
endMonth = f"{endTime:%m}"
endDay = f"{endTime:%d}"
endHour = f"{endTime.hour:02d}"
endMinute = f"{endTime.minute:02d}"
endSecond = f"{endTime.second:02d}"

### organization 
#UNIVERSITY OF FLORIDA
#organization = 'da0f0bfb-82ad-4a1e-9dfa-a31c93170110'
#probes = '0004a30b00214f9c'

#YARA
#organization = 'b7e58cc6-b6ea-41e0-a7a8-7c5703224bfb'
#probes = '0004a30b0021651d'
#probes = '0004a30b00216f5b'


#RCD Santa Cruz
#organization = '6a42d72c-76db-4359-b7bd-50a4c72c9e6c'
#probes = '0004a30b00215aa1'

#NuWay CoOp
organization = '7e9e3c4b-5bda-474a-848a-609a53a0a197'
probes = '0004a30b002166b0'

headers = {
	'Accept': 'application/json',
	'Authorization': 'Bearer '+str(accessToken),
	'x-api-key': str(apiKey)
	
}

#r = requests.get('https://api.teralytic.io/alpha/v1/soils/', params={'geometry': 'Point(-96.86614 33.154564)'}, headers = headers)
#r  = requests.get('https://api.teralytic.io/v1/organizations/', headers = headers)

r = requests.get('https://api.teralytic.io/alpha/v1/organizations/'+str(organization)+'/readings?start_date='+str(startYear)+'-'+str(startMonth)+'-'+str(startDay)+'T'+str(startHour)+'%3A'+str(startMonth)+'%3A00-00%3A00'+'&end_date='+str(endYear)+'-'+str(endMonth)+'-'+str(endDay)+'T'+str(endHour)+'%3A'+str(endMonth)+'%3A00-00%3A00'+'&probes='+str(probes)+'&extended=true', params={}, headers = headers)
#print(r)

dic = r.json()
#print(dic)

vwc6List  = []
vwc18List = []
vwc36List = []
aw6List = []
aw18List = []
aw36List = []
fc6List = []
fc18List = []
fc36List = []
pwp6List = []
pwp18List = []
pwp36List = []

for i in dic:
	#print(i)
	readings = i['readings']
	#print(readings)
	timestamp = i['timestamp']
	#print(timestamp)
	vwc6 = readings[0]['moisture']
	vwc18 = readings[1]['moisture']
	vwc36 = readings[2]['moisture']
	vwc6List.append(vwc6)
	vwc18List.append(vwc18)
	vwc36List.append(vwc36)
	irrigation  = i['irrigation']
	aw_6 = irrigation['aw_6']
	aw_18 = irrigation['aw_18']
	aw_36 = irrigation['aw_36']
	aw6List.append(aw_6)
	aw18List.append(aw_18)
	aw36List.append(aw_36)
	fc_6 = irrigation['fc_6']
	fc_18 = irrigation['fc_18']
	fc_36 = irrigation['fc_36']
	fc6List.append(fc_6)
	fc18List.append(fc_18)
	fc36List.append(fc_36)
	pwp_6  = irrigation['pwp_6']
	pwp_18 = irrigation['pwp_18']
	pwp_36 = irrigation['pwp_36']
	pwp6List.append(pwp_6)
	pwp18List.append(pwp_18)
	pwp36List.append(pwp_36)

##################################################	
###VOLUMETRIC WATER CONTENT
# Filter  out Null Values 
vwc6List = list(filter(lambda a: a!= None, vwc6List))
vwc18List = list(filter(lambda a: a!= None, vwc18List))
vwc36List = list(filter(lambda a: a!= None, vwc36List))

print("6in VWC")
#print(vwc6List)
try:
	vwc6Avg = statistics.mean(vwc6List)
	vwc6Avg = vwc6Avg*100
except:
	vwc6Avg = None
print(vwc6Avg)
###########
print("18in VWC")
#print(vwc18List)
try:
	vwc18Avg = statistics.mean(vwc18List)
	vwc18Avg = vwc18Avg*100
except:
	vwc18Avg = None
print(vwc18Avg)
###############
print("36in VWC")
#print(vwc36List)
try:
	vwc36Avg = statistics.mean(vwc36List)
	vwc36Avg = vwc36Avg * 100
except:
	vwc36Avg = None	
print(vwc36Avg)

# now filter the irrigation condition based on VWC
if checkMoistureHour == True and vwc6Avg <= moistureThresh:
        irrigationOn = True
        print("Irrigation condition met, now watering")
        irrigationAmt = controllerParams['config']['user']['watering_duration_seconds']
        print("Apply water for " + str(irrigationAmt)+" seconds.")


#############################
#available water capacity (AWC)
##try:
##        aw6List = list(filter(lambda a: a!= None, aw6List))
##        #print(aw6List)
##        aw6Avg = statistics.mean(aw6List)
##        print("6in Available Water (inches) : " + str(aw6Avg))
##except:
##        aw6List = None
##        aw6Avg = None
##        
##aw18List = list(filter(lambda a: a!= None, aw18List))
###print(aw18List)
##aw18Avg = statistics.mean(aw18List)
##print("18in Available Water (inches) : " + str(aw18Avg))
##aw36List = list(filter(lambda a: a!= None, aw36List))
###print(aw36List)
##aw36Avg = statistics.mean(aw36List)
##print("36in Available Water (inches) : " + str(aw36Avg))
################################
##fc6List = list(filter(lambda a: a!= None, fc6List))
###print(fc6List)
##fc6Avg = statistics.mean(fc6List)
##print("6in Field Capacity (inches) : " + str(fc6Avg))
##fc18List = list(filter(lambda a: a!= None, fc18List))
###print(fc18List)
##fc18Avg = statistics.mean(fc18List)
##print("18in Field Capacity (inches) : " + str(fc18Avg))
##fc36List = list(filter(lambda a: a!= None, fc36List))
###print(fc36List)
##fc36Avg = statistics.mean(fc36List)
##print("36in Field Capacity (inches) : " + str(fc36Avg))
################################
##pwp6List = list(filter(lambda a: a!= None, pwp6List))
###print(pwp6List)
##pwp6Avg = statistics.mean(pwp6List)
##print("6in Permanent Wilting Point: " + str(pwp6Avg))
##pwp18List = list(filter(lambda a: a!= None, pwp18List))
###print(pwp18List
##pwp18Avg = statistics.mean(pwp18List)
##print("18in Permanent Wilting Point: " + str(pwp18Avg))
##pwp36List = list(filter(lambda a: a!= None, pwp36List))
###print(pwp36List)
##pwp36Avg = statistics.mean(pwp36List)
##print("36in Permanent Wilting Point: " + str(pwp36Avg))
