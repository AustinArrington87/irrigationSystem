# irrigationSystem
Raspberry Pi code for automated irrigation system 

MANUAL START UP ==> Trigger script which threads together the system's files

$ cd ~/Desktop/smartIrrigation

$ sudo python3.6 plantGroupSmartIrrigation.py

====================================================

RUN SCRIPT ON BOOTUP ==> Update Pi so that irrigationSystem starts on boot
$ sudo crontab -e
@reboot sudo python3.6 /home/pi/Desktop/irrigationSystem/plantGroupSmarrtIrrigation.py &


====================================================

REST API ==> Add zones, controllers, valves, and probes for your irrigationSystem
http://app.plantgroup.co/api/
- create valves, probes, and controllers at app.plantgroup.co
- Add Thingspeak Write API Key to tsUpdate.py
- Add Valve MCUid (http://app.plantgroup.co/admin/plant/valve/) to wateringProtocol.py
- TS Valve Channel ID to use  in  PG web app: 820394
- Add Controller MCUid (http://app.plantgroup.co/admin/plant/controller) into irrigation config API endpoint ("http://app.plantgroup.co/api/controllers/<controller_MCUid>/config/") in order to program irrigation automation paramters from the web app into data.json (the config file on Pi)
- Add Thingspeak Channel ID to Probe (http://app.plantgroup.co/admin/plant/probe/)
- If getting soil moisture data from API, update params in serialJSONFunction.py (i.e. 'https://api.teralytic.io/alpha/v1/' for Teralytic sensor API)


# RASPBERRY PI ENVIRONMENT INSTALLATION 

INSTALLING PYTHON 3.6
$ wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
$ tar xf Python-3.6.5.tgz
$ cd Python-3.6.5/
$ ./configure
$ make -j4
$ sudo make install

then:

$ sudo apt-get install libssl-dev
$ cd Python-3.6.5/
$ sudo ./configure
$ sudo make altinstall

then need to install serial, colorama, and requests: 

$ sudo pip3 install serial
$ sudo pip3 install colorama
$ sudo pip3 install requests
$ sudo pip3 install Rpi.GPIO

