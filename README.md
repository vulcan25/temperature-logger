A temperature logger designed to work with the DS18B20 and the raspberry pi.  This application logs temperatures to a flask endpoint.

## Pre-requirements


You will need to wire up the DS18B20 (or several) as per [this tutorial](http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/).
Follow the wiring diagram `Wiring for SSH Terminal Output`.  If this worked, you should be able to see the following information at the terminal for each sensor:

	pi@raspberry:~ $ cat /sys/bus/w1/devices/28-0000077b5cfd/w1_slave 
	53 00 4b 46 7f ff 0d 10 d4 : crc=d4 YES
	53 00 4b 46 7f ff 0d 10 d4 t=5187

Note the `28-0000077b5cfd` part will differ per sensor.  5.187 degress celcius is the temperature from this one.

## Install

Create a python 3 virtualenv, and install:

	python -m venv temperature-logger
	. venv/bin/activate
	pip install -e git+https://github.com/vulcan25/temperature-logger#egg=temperature-logger

## Usage

	from temperature_logger import Report
	from time import sleep

You should then define a list of your own sensors:

	sensors = ['/sys/bus/w1/devices/28-0000077aae57/w1_slave',
	           '/sys/bus/w1/devices/28-0000077aa8d5/w1_slave',
	           '/sys/bus/w1/devices/28-0000077b5cfd/w1_slave',
	           ]

Create a Report object, passing the endpoint and those `sensors`:

	r = Report('http://raspberry:5000/temperature/temp', sensors )

At this point you can define the following loop, which will update the temperature every 60 seconds.  If it fails to connect to the endpoint, the readings will be stored in memory until the endpoint becomes available.

	while True:    
	    print ('-> Reading temperature ...')
	    r.read_temps()
	    print ('-> Submitting Temperatures ...')
	    r.submit()
	    print ('-> Items in Queue: ', len(r.readings))
	    sleep(60)

