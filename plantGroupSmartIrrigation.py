###MultiThread PlantGroup Smart Irrigation###
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

import threading
import time
import json

from getConfigJSON import intervals
from serialJSONFunction import serialRead
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
