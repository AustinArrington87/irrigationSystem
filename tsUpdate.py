#####Thingspeak Function#####
####W. Weiner 08-Oct-2018####

import urllib.request
import json
import time

tsAPI='SMQ9OUC4A53N22JE'

def tsUpdate():
    while True:
        try:
            file=open('data.json','r')
            data1=file.read()
            jsonFormat=json.loads(data1)
            file.close()
            file2=open('serial.json','r')
            data2=file2.read()
            serVars=json.loads(data2)
            file2.close()
            tsUpdate = jsonFormat['tsUpdate']
            moist = str(serVars['moisture'])
            temp = str(serVars['temp'])
            bat = str(serVars['bat'])
            tsURL = 'https://api.thingspeak.com/update?api_key='+tsAPI+'&field1='+moist+'&field2='+bat+'&field3='+temp
            urllib.request.urlopen(tsURL)
            print(tsUpdate)
            print("thingspeak updated")
        except:
            print("thingspeak NOT UPDATED!!!!!!")
        time.sleep(tsUpdate)
