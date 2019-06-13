###Intervals Function######
##W. Weiner 07-Oct-2018####

import serial
import time
import ast
import urllib.request
import json
import datetime

url = "http://app.plantgroup.co/api/controllers/Frito-backyard/config/"

def intervals():
        while True:
                try:
                        def secConv(x):
                                secs = time.strptime(x,'%H:%M:%S')
                                return datetime.timedelta(hours=secs.tm_hour,
                                        minutes=secs.tm_min,
                                        seconds=secs.tm_sec).total_seconds()
                        try:
                                response = urllib.request.urlopen(url).read()
                        except Exception as err:
                                print("There was an error calling this URL")
                                print(err)
                                file=open('urlError.txt','w')
                                file.write(str(err))
                                file.close()
                        resp2=response.decode('utf-8')
                        jsonForm = json.loads(resp2)

                        var={}
                        stop=[]
                        begin=[]
                        var['tsUpdate']=((jsonForm["config"]["system"]["sync_interval_seconds"]))
                        var['sysClock']=(jsonForm["config"]["system"]["system_clock_seconds"])
                        var['soilThresh']=(jsonForm["config"]["user"]["soil_moisture_threshold"])
                        var['waterDelay']=(jsonForm["config"]["user"]["watering_delay_seconds"])
                        var['waterDuration']=(jsonForm["config"]["user"]["watering_duration_seconds"])
                        var['serverTime'] = secConv(jsonForm["local_time"])

                        intervals = len(jsonForm["config"]["user"]["watering_schedule"])
                    
                        for i in range(0,intervals):
                                stop.append(secConv((jsonForm["config"]["user"]["watering_schedule"][i]["end"])+":00"))
                                begin.append(secConv((jsonForm["config"]["user"]["watering_schedule"][i]["begin"])+":00"))
                                var['stop']=stop
                                var['start']=begin
                        
                        with open('data.json','w') as outfile:
                                json.dump(var,outfile)
                                print("wrote to 'data.json'")
                                outfile.close()
                                
                        print('asleep')
                        time.sleep(var['sysClock'])
                except Exception as exp:
                        file=open('errorReport.txt','w')
                        file.write(str(exp))
                        file.close()
                        
                                

#not using this function below
def fileRead():
    file=open('data.json','r')
    data1=file.read()
    jsonFormat=json.loads(data1)
    print(jsonFormat)
    return jsonFormat
