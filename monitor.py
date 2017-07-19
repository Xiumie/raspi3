#!/usr/bin/env python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys, os
import subprocess

class Monitor(object):
    def __init__(self, ud_angle=60, rl_angle=10, updown_pin=20, rightleft_pin=21):
        # 初始化配置
        self.__updown_pin = updown_pin
        self.__rightleft_pin = rightleft_pin
        self.__ud_angle = ud_angle
        self.__rl_angle = rl_angle
        # up down right left 步进幅度
        self.__adjust = 5
        
        # GPIO.cleanup()
        # 设置GPIO模式&&忽略警报
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__updown_pin, GPIO.OUT, initial=False)
        GPIO.setup(self.__rightleft_pin, GPIO.OUT, initial=False)
        self.__ud = GPIO.PWM(self.__updown_pin, 50) # 50Hz---20ms
        self.__rl = GPIO.PWM(self.__rightleft_pin, 50)
        self.__ud.start(0)
        self.__rl.start(0)
        time.sleep(1)
        self.set_angle(self.__ud_angle, self.__rl_angle)
    
    # 设置云台角度
    def set_angle(self, ud_angle, rl_angle):
        if ud_angle > 180:
            ud_angle = 180
        if ud_angle < 0:
            ud_angle = 0
        if rl_angle > 180:
            rl_angle = 180
        if rl_angle < 0:
            rl_angle = 0
        
        # sg90舵机 20ms基准脉冲，0.5ms---0° 2.5ms---180° 0.5/20*100=2.5 2.5/20*100=12.5
        self.__ud_angle = ud_angle
        self.__rl_angle = rl_angle
        self.__ud.ChangeDutyCycle(2.5 + 10*self.__ud_angle/180)
        self.__rl.ChangeDutyCycle(2.5 + 10*self.__rl_angle/180)
        time.sleep(0.2)
        # 回归pwm，可有可无，不设置不影响舵机转动角度
        self.__ud.ChangeDutyCycle(0)
        self.__rl.ChangeDutyCycle(0)
        time.sleep(1)
    
    # 停止
    def stop(self):
        self.__ud.stop()
        self.__rl.stop()
        GPIO.cleanup()
    
    def up(self):
        # 当角度值不超范围时 运动
        if 0 < self.__ud_angle <= 180:
            self.__ud_angle = self.__ud_angle - self.__adjust
        else:
            return
        self.__ud.ChangeDutyCycle(2.5 + 10*self.__ud_angle/180)
        time.sleep(0.1)
        self.__ud.ChangeDutyCycle(0)
        time.sleep(0.1)
        
    def down(self):
        if 0 <= self.__ud_angle < 180:
            self.__ud_angle = self.__ud_angle + self.__adjust
        else:
            return
        self.__ud.ChangeDutyCycle(2.5 + 10*self.__ud_angle/180)
        time.sleep(0.1)
        self.__ud.ChangeDutyCycle(0)
        time.sleep(0.1)
        
    def right(self):
        if 0 < self.__rl_angle <= 180:
            self.__rl_angle = self.__rl_angle - self.__adjust
        else:
            return
        self.__rl.ChangeDutyCycle(2.5 + 10*self.__rl_angle/180)
        time.sleep(0.1)
        self.__rl.ChangeDutyCycle(0)
        time.sleep(0.1)
        
    def left(self):
        if 0 <= self.__rl_angle < 180:
            self.__rl_angle = self.__rl_angle + self.__adjust
        else:
            return
        self.__rl.ChangeDutyCycle(2.5 + 10*self.__rl_angle/180)
        time.sleep(0.1)
        self.__rl.ChangeDutyCycle(0)
        time.sleep(0.1)
        
if __name__ == '__main__':
    clouldmon = Monitor()
    try:
        while True:
            os.chdir("/var/www/html/img")
            # 时间判断 08:00:00-20:00:00
            if 80000 < int(time.strftime("%H%M%S")) < 200000:
                # 调用shell拍照
                cmd = 'sudo raspistill -o main.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                # 调用shell使用scp传送到远程服务器
                # cmd = 'scp -P 23 filepath username@ip:filepath'
                # pid = subprocess.call(cmd, shell=True)
                print time.strftime("%H:%M:%S")+" ok"
                time.sleep(60*10)
            else:
                cmd = 'sudo raspistill -o 1.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,45)
                cmd = 'sudo raspistill -o 2.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,90)
                cmd = 'sudo raspistill -o 3.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,135)
                cmd = 'sudo raspistill -o 4.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,170)
                cmd = 'sudo raspistill -o 5.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)

                print time.strftime("%H:%M:%S")+" ok"
                time.sleep(60*10)
                
                cmd = 'sudo raspistill -o 5.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,135)
                cmd = 'sudo raspistill -o 4.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,90)
                cmd = 'sudo raspistill -o 3.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,45)
                cmd = 'sudo raspistill -o 2.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                clouldmon.set_angle(60,10)
                cmd = 'sudo raspistill -o 1.jpg -t 1000 -rot 180'
                pid = subprocess.call(cmd, shell=True)
                
                print time.strftime("%H:%M:%S")+" ok"
                time.sleep(60*10)
            
    except Exception, e:
        clouldmon.stop()
        print str(e)
        
        
        

