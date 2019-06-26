#############Post Function###############
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
    
    
