#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as gpio
import time, sys, os, string, subprocess
import requests, json, socket, urllib
from multiprocessing import Value, Queue, Process

row = [5,6]
col = [13,19]
keys = [25,24,19,18]

def get_key(trytime = 0.03):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    while(True):
        num = 0
        time.sleep(0.2)
        for i in range(len(col)):
            gpio.setup(row[0], gpio.OUT)
            gpio.setup(row[1], gpio.OUT)
            gpio.setup(col[0], gpio.IN, pull_up_down=gpio.PUD_UP)
            gpio.setup(col[1], gpio.IN, pull_up_down=gpio.PUD_UP)
            gpio.output(row[0],gpio.LOW)
            gpio.output(row[1],gpio.LOW)
            if gpio.input(col[i]) is gpio.LOW:
                time.sleep(trytime)
                if gpio.input(col[i]) is gpio.LOW:
                    num = col[i]
                    #print '%s:%s' %(i,num)
                    gpio.setup(col[0], gpio.OUT)
                    gpio.setup(col[1], gpio.OUT)
                    gpio.setup(row[0], gpio.IN, pull_up_down=gpio.PUD_UP)
                    gpio.setup(row[1], gpio.IN, pull_up_down=gpio.PUD_UP)
                    gpio.output(col[0],gpio.LOW)
                    gpio.output(col[1],gpio.LOW)
                    
                    for i in range(len(row)):
                        if gpio.input(row[i]) is gpio.LOW:
                            time.sleep(trytime)
                            if gpio.input(row[i]) is gpio.LOW:
                                num = num + row[i]
                                #print '2:'
                                #print num
                                # while gpio.input(row[i]) is gpio.LOW:
                                    # time.sleep(0.5)
                                gpio.cleanup()
                                return num

if __name__ == '__main__':
    cal = 1
    while(True):
        key = get_key()
        if key is keys[0]:
            print key
            key = get_key(3.0)
            if key is keys[0]:
                print "shutdown"
                cmd = "sudo poweroff"
                pid = subprocess.call(cmd, shell=True)
        elif key is keys[1]:
            if cal is 1:
                cal = 2
                print "IPProxy.py"
                cmd = "python /home/pi/IPProxyPool/IPProxyPool_py2/IPProxy.py"
                
                pid = subprocess.call(cmd, shell=True)
            elif cal is 2:
                cal = 3
                print "youmzi2.py"
                cmd = "python /home/pi/py2/youmzi2.py"
                
                pid = subprocess.call(cmd, shell=True)
        elif key is keys[2]:
            print "reboot"
            cmd = "sudo reboot"
            pid = subprocess.call(cmd, shell=True)
        elif key is keys[3]:
            print "5110.py"
            cmd = "python /home/pi/py2/5110.py"
            pid = subprocess.call(cmd, shell=True)
        time.sleep(1)
