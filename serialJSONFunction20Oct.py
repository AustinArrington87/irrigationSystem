###Serial Function###
###W. Weiner 07-Oct-2018###

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
