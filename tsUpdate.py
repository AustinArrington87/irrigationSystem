#####Thingspeak Function#####
import urllib.request
import json
import time

# ENTER THINGSPEAK WRITE API KEY
#Backyard
#tsAPI='SMQ9OUC4A53N22JE'

#Teralytic 
tsAPI='9KTNBVCOWOBEZ79B'

def tsUpdate():
    while True:
        try:
            file=open('/home/pi/Desktop/irrigationSystem/data.json','r')
            data1=file.read()
            jsonFormat=json.loads(data1)
            file.close()
            file2=open('/home/pi/Desktop/irrigationSystem/serial.json','r')
            data2=file2.read()
            serVars=json.loads(data2)
            file2.close()
            tsUpdate = jsonFormat['tsUpdate']
            moist = str(serVars['moisture'])
            tsURL = 'https://api.thingspeak.com/update?api_key='+tsAPI+'&field1='+moist
            urllib.request.urlopen(tsURL)
            print(tsUpdate)
            print("thingspeak updated")
        except:
            print("thingspeak NOT UPDATED!!!!!!")
        time.sleep(tsUpdate)
