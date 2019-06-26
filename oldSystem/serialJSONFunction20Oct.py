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



ser = serial.Serial(port='/dev/ttyAMA0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            )
probeVars="{'moisture':0,'temp':0,'bat':0,'ID':0}"


def serialRead():
    while True:
        x=ser.readline()
        global probeVars
        probeVars=x.decode('utf-8')
        if len(x)>0:
            probeVars=ast.literal_eval(probeVars)
            print(probeVars)
            with open('serial.json','w') as outfile:
                json.dump(probeVars,outfile)
                print("wrote to 'serial.json'")
