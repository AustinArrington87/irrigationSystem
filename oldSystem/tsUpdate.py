#####Thingspeak Function#####
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
