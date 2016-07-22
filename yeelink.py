#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import string
import requests
import json
import RPi.GPIO as GPIO 
from BMP180 import BMP180

tmp_set = 45.0

def bmp180():
	bmp=BMP180()
	bmp180temp=bmp.read_temperature()
	bmp180pre=bmp.read_pressure()
	bmp180alt=bmp.read_altitude()
	return bmp180temp,bmp180pre,bmp180alt

def get_dht():
	# have to delay 1s to
	time.sleep(1)

	data=[]
	j=0
	#start work have low delay > 18ms
	GPIO.setup(12,GPIO.OUT)
	GPIO.output(12,GPIO.LOW)
	time.sleep(0.02)
	GPIO.output(12,GPIO.HIGH)
	#have high 20ms-40ms
	for i in range(40):
		pass

	#wait to response
	GPIO.setup(12,GPIO.IN)


	while GPIO.input(12)==1:
		continue


	while GPIO.input(12)==0:
		continue

	while GPIO.input(12)==1:
		continue
	#get data

	while j<40:
		k=0
		while GPIO.input(12)==0: #low start
			continue
		
		while GPIO.input(12)==1:
			k+=1
			if k>150:break  # 26us-28us is 0, 70us is 1
		if k<22:
			data.append(0)
		else:
			data.append(1)
		j+=1

	#get temperature
	humidity_bit=data[0:8]
	humidity_point_bit=data[8:16]
	temperature_bit=data[16:24]
	temperature_point_bit=data[24:32]
	check_bit=data[32:40]

	humidity=0
	humidity_point=0
	temperature=0
	temperature_point=0
	check=0


	for i in range(8):
		humidity+=humidity_bit[i]*2**(7-i)
		humidity_point+=humidity_point_bit[i]*2**(7-i)
		temperature+=temperature_bit[i]*2**(7-i)
		temperature_point+=temperature_point_bit[i]*2**(7-i)
		check+=check_bit[i]*2**(7-i)

	tmp=humidity+humidity_point+temperature+temperature_point
	if check==tmp and humidity!=0:
		return temperature, humidity
	else:
		print "something is worong!",humidity,humidity_point,temperature,temperature_point,check
		return False, False

def get_CPU_temp():
	f = file("/sys/class/thermal/thermal_zone0/temp")
	temp = float(f.read().strip("\n"))/1000
	return "%.3f" % temp

def get_CPU_use():
	return os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").read().strip("\n")

def get_GPU_temp():
	status = os.popen("/opt/vc/bin/vcgencmd measure_temp").read().strip("\n")
	return status.split("=")[1].replace("\'C", "")

if __name__ == '__main__':
	# set gpio mode and ignore pin warnings setmode as out 
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.OUT)
	# get cpu_temp,gpu_temp,and
	cpu_tmp = get_CPU_temp()
	cpu_use = get_CPU_use()
	gpu_tmp = get_GPU_temp()
	# dh11 temp and humi
	temp, humi = get_dht()
	while temp == False:
		time.sleep(2)
		temp, humi = get_dht()
	print "temp is", temp,"wet is",humi,"%"
	
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/391878/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': temp}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	
	if r.status_code == 200:
		print 'dht temp success'
	else:
		print 'dht temp failure'
	
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/391879/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': humi}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	
	if r.status_code == 200:
		print 'dht humi success'
	else:
		print 'dht humi failure'

	print """Current status:
		CPU Temperature : %s\'C
		CPU Use : %s%c
		GPU Temperature : %s\'C""" % (cpu_tmp, cpu_use, 0x25, gpu_tmp)

	# check cpu's temp to on/off 
	if string.atof(cpu_tmp) > tmp_set:
		GPIO.output(18, True)
	elif string.atof(cpu_tmp) <= tmp_set:
		GPIO.output(18, False)
	else:
		pass

	# send CPU temp
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/391761/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': cpu_tmp}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	if r.status_code == 200:
		print 'cpu temp success'
	else:
		print 'cpu temp failure'

	# send CPU use
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/391841/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': cpu_use}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	if r.status_code == 200:
		print 'cpu use success'
	else:
		print 'cpu use failure'

	# send GPU temp
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/391842/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': gpu_tmp}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	if r.status_code == 200:
		print 'gpu temp success'
	else:
		print 'gpu temp failure'
	
	# BMP180 
	(bmp180temp,bmp180pre,bmp180alt)=bmp180()
	print bmp180temp,bmp180pre,bmp180alt
	
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/392414/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': bmp180temp}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	if r.status_code == 200:
		print 'BMP180 temp success'
	else:
		print 'BMP180 temp failure'

	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/392415/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': bmp180pre}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	if r.status_code == 200:
		print 'BMP180 pre success'
	else:
		print 'BMP180 pre failure'

