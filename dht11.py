# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time
import requests
import json 

def get_dht():
	# have to delay 1s to
	time.sleep(1)

	data=[]
	j=0
	#start work have low delay > 18ms
	gpio.setup(12,gpio.OUT)
	gpio.output(12,gpio.LOW)
	time.sleep(0.02)
	gpio.output(12,gpio.HIGH)
	#have high 20ms-40ms
	for i in range(40):
		pass

	#wait to response
	gpio.setup(12,gpio.IN)


	while gpio.input(12)==1:
		continue


	while gpio.input(12)==0:
		continue

	while gpio.input(12)==1:
		continue
	#get data

	while j<40:
		k=0
		while gpio.input(12)==0: #low start
			continue
		
		while gpio.input(12)==1:
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
		return False

if __name__ == '__main__':
	gpio.setwarnings(False)
	gpio.setmode(gpio.BCM)
	
	temp, humi = get_dht()
	while temp == False:
		time.sleep(2)
		temp, humi = get_dht()
	print "temperature is", temp,"wet is",humi,"%"
	
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/391878/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': temp}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	
	print 'response status: %d' %r.status_code
	
	apiurl = 'http://api.yeelink.net/v1.1/device/349618/sensor/391879/datapoints'
	apiheaders = {'U-Apikey': '', 'content-type': 'application/json'}
	payload = {'value': humi}
	r = requests.post(apiurl, headers=apiheaders, data=json.dumps(payload))
	
	print 'response status: %d' %r.status_code
