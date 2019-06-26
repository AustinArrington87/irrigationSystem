###Intervals Function######
# Copyright (C) 2019 PLANT GROUP, LLC | www.plantgroup.co

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
