###MultiThread PlantGroup Smart Irrigation###
########W. Weiner 09-Oct-2018################

import threading
import time
import json

from getConfigJSON20Oct import intervals
from serialJSONFunction20Oct import serialRead
from tsUpdate import tsUpdate
from wateringProtocol import watering

configGrab = threading.Thread(name='configGrab',target=intervals)
probeRead = threading.Thread(name='probeRead',target=serialRead)
irrigate = threading.Thread(name='irrigate',target=watering)
ts = threading.Thread(name='dataUpdate',target=tsUpdate)


configGrab.start() #comment out for off the grid version
probeRead.start()
irrigate.start() #need to open 'wateringProtocol' to comment out start/stop
ts.start() #comment out for off the grid version
