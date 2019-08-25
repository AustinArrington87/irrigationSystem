# irrigationSystem
Raspberry Pi code for automated irrigation system 

RUN SCRIPT ON BOOTUP 
$ sudo crontab -e
@reboot sudo python3.6 /home/pi/Desktop/irrigationSystem/plantGroupSmarrtIrrigation.py &


REST API 
http://app.plantgroup.co/api/
- create valves, probes, and controllers at app.plantgroup.co

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

