###Serial Function###
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
import json
import requests
import statistics
from datetime import datetime, timezone, timedelta

def getProbeMoisture():
    #teralytic sensor & API configuration
    token_url = "https://auth.teralytic.io/token"
    client_id = 'XXXX'
    client_secret = 'XXXX'
    # soil API call
    apiKey = 'XXXX'

    #step A, B - single call with client credentials as the basic auth header - will return access_token
    data = {'grant_type': 'client_credentials'}

    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

    tokens = json.loads(access_token_response.text)

    #print(tokens)

    accessToken = tokens['access_token']
    #print(accessToken)

    #start in the past
    startTime = datetime.now() - timedelta(hours = 4)
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

    #Active Teralytic Probes
     
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
    #organization = '7e9e3c4b-5bda-474a-848a-609a53a0a197'
    #probes = '0004a30b002166b0'
    
    #RIL
    organization = '6b28ee93-cc97-4d7e-9095-20b3d2503fca'
    probes = '0004a30b002385b3'

    headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer '+str(accessToken),
            'x-api-key': str(apiKey)	
    }

    r = requests.get('https://api.teralytic.io/alpha/v1/organizations/'+str(organization)+'/readings?start_date='+str(startYear)+'-'+str(startMonth)+'-'+str(startDay)+'T'+str(startHour)+'%3A'+str(startMonth)+'%3A00-00%3A00'+'&end_date='+str(endYear)+'-'+str(endMonth)+'-'+str(endDay)+'T'+str(endHour)+'%3A'+str(endMonth)+'%3A00-00%3A00'+'&probes='+str(probes)+'&extended=true', params={}, headers = headers)
    #print(r)
    dic = r.json()
    #print(dic)

    #6in VWC list
    vwc6List = []
    # fill in 6in moisture values in empty from sample of last 4 hrs
    try:
        for i in dic:
            readings = i['readings']
            vwc6 = readings[0]['moisture']
            vwc6List.append(vwc6)
    except:
        try:
            with open('/home/pi/Desktop/irrigationSystem/serial.json') as json_file:
                moistureData = json.load(json_file)
                vwc6 = moistureData["moisture"]
        except:
            vwc6 = None

        vwc6List.append(vwc6)
        print("Issue with probe.  Error: "+str(r))

    #filter out null values from list
    vwc6List = list(filter(lambda a: a!= None, vwc6List))
    print("6in VWC: ")
    global vwc6Avg
    try:
        vwc6Avg = statistics.mean(vwc6List)
        vwc6Avg = vwc6Avg*100
        print("Soil Moisture Value (successful): "+str(vwc6Avg))
    except:
        vwc6Avg = None #probe not working if you get this part of code
        print("Soil Moisture Value (NOT successful): "+str(vwc6Avg))
        
    try:
        if vwc6Avg > 100:
            with open('/home/pi/Desktop/irrigationSystem/serial.json') as json_file:
                vwc6Avg = json.load(json_file)
                vwc6Avg = vwc6Avg["moisture"]
    except:
        pass

    print(vwc6Avg)

    #dictionary format for json outfile
    global moistureSample
    moistureSample = {'moisture': vwc6Avg}

def serialRead():
    while True:
        try:
            getProbeMoisture()
            try:
                file=open('/home/pi/Desktop/irrigationSystem/data.json','r')
                data1=file.read()
                jsonFormat=json.loads(data1)
                file.close()
                systemCycle = jsonFormat['sysClock']
                print(systemCycle)
                with open('/home/pi/Desktop/irrigationSystem/serial.json', 'w') as fp:
                    json.dump(moistureSample, fp)
                    print("Wrote moisture value to serial.json")
            except:
                print("Moisture Read Error")
        except Exception as excep3:
                file5=open('/home/pi/Desktop/irrigationSystem/terraProbeError.txt','w')
                file5.write(str(excep2))
                file5.close()      
        time.sleep(systemCycle*5)
            
