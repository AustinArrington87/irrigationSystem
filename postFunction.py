#############Post Function###############
########W. Weiner 15Oct2018##############

import datetime
import requests

def postStart(timestamp,valve):
    post=requests.post("http://app.plantgroup.co/api/valves/"+str(valve)+"/record_event/"
                       , data={"event_type":1,"created_at":timestamp})

def postStop(timestamp,valve):
    post=requests.post("http://app.plantgroup.co/api/valves/"+str(valve)+"/record_event/"
                       , data={"event_type":2,"created_at":timestamp})

def postStamp(valve,event):
    global epoch
    epoch = datetime.datetime.now().timestamp()
    print(epoch)

    funcArr = {1: postStart,
               2: postStop}

    run=funcArr.get(event)
    run(epoch,valve)
    
    
