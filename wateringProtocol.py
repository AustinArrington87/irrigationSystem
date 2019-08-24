####Watering Protocol####
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
import json
import time
import datetime
import RPi.GPIO as GPIO
import time
from postFunction import postStart,postStop,postStamp
from colorama import Fore,Back,Style

#mcuID for PG Valve (On/off Events)
valve = "Teralytic-1"

motorPin = 11 #need to update pin to which will control motor

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorPin,GPIO.OUT)

GPIO.output(motorPin,GPIO.LOW)
soilNow='wet'
waterCount=0
delayCount=0
delayGo='no'
wateringVar=0

def watering():
    while True:
        #name global variables for loop control,initialized outside of function
        global soilNow
        global waterCount
        global delayCount
        global delayGo
        global wateringVar

        try:
        
            try:
                file1=open('data.json','r')
                data1=file1.read()
                config=json.loads(data1) #config contains the json variables from app.plantgroup
                file1.close()
            except Exception as excep:
                file3=open('errorWater.txt','w')
                file3.write(str(excep))
                file3.close()
                print(Fore.RED+"Config error experienced: "+str(excep))
                print(Style.RESET_ALL)
                
            try:
                file2=open('serial.json','r')
                data2=file2.read()
                probeVar=json.loads(data2) #probeVar contains probe variables
                file2.close()
            except Exception as excep1:
                file4=open('errorProb.txt','w')
                file4.write(str(excep1))
                file4.close()
                print(Fore.RED+"Probe error experienced: "+str(excep1))
                print(Style.RESET_ALL)

            intervals=len(config['stop'])

            if not config['stop']:
                tim='bad'
            else:
                for i in range(0,intervals):
                    if (config['serverTime']<=config['stop'][i] and
                        config['serverTime']>=config['start'][i]):
                        tim='good'
                        print('time good')
                        if delayGo=='yes':
                            print('proceed to delay')
                            GPIO.output(motorPin,GPIO.LOW)
                            delayCount=delayCount+1
                            print(delayCount)
                            if delayCount>=(config['waterDelay']/config['sysClock']):
                                delayCount=0
                                delayGo='no'
                                print('delay over')
                            break
                        #put soilThresh check here
                        if probeVar['moisture']<=float(config['soilThresh']):
                            soilNow='dry'
                            print('soil is dry')
                        else:
                            print('soil is wet')
                            #put watering portion of code here
                        if (soilNow=='dry' and delayGo=='no'):
                            print("watering time")
                            wateringVar=1
                            GPIO.output(motorPin,GPIO.HIGH)
                            waterCount=waterCount+1
                            if waterCount==1: #comment out for off-grid
                                postStamp(valve,1) #comment out for off-grid
                            print(waterCount)
                            if waterCount >= (config['waterDuration']/config['sysClock']):
                                print('watering ended')
                                postStamp(valve,2) #comment out for off-grid
                                GPIO.output(motorPin,GPIO.LOW)
                                soilNow='wet'
                                waterCount=0
                                delayGo='yes'
                                wateringVar=0
                        break
                    else:
                        tim='bad'
                        print('time bad end of watering loop')
            #turn everything off if interval is bad
            if (tim=='bad'):
                print('time bad interval check')
                if wateringVar == 1: #comment out for off-grid
                    postStamp(valve,2) #comment out for off-grid
                    wateringVar = 0 #comment out for off-grid
                GPIO.output(motorPin,GPIO.LOW)
                soilNow='wet'
                waterCount=0
                delayCount=0
                delayGo='no'
                wateringVar=0
            print('sleeping')
            time.sleep(config['sysClock'])
            print('awake')
        except Exception as excep2:
                file4=open('errorHighLevelWater.txt','w')
                file4.write(str(excep2))
                file4.close()
                