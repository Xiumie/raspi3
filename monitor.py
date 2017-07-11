#!/usr/bin/env python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

class Monitor(object):
    def __init__(self, updown_pin=20, rightleft_pin=21, ud_angle=60, rl_angle=90):
        # 初始化配置
        self.__updown_pin = updown_pin
        self.__rightleft_pin = rightleft_pin
        self.__ud_angle = ud_angle
        self.__rl_angle = rl_angle
        
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
        if 0 <= self.__ud_angle < 180:
            self.__ud_angle = self.__ud_angle - 10
        else:
            return
        self.__ud.ChangeDutyCycle(2.5 + 10*self.__ud_angle/180)
        time.sleep(0.02)
        self.__ud.ChangeDutyCycle(0)
        time.sleep(0.5)
        
    def down(self):
        if 0 <= self.__ud_angle < 180:
            self.__ud_angle = self.__ud_angle + 10
        else:
            return
        self.__ud.ChangeDutyCycle(2.5 + 10*self.__ud_angle/180)
        time.sleep(0.02)
        self.__ud.ChangeDutyCycle(0)
        time.sleep(0.5)
        
    def right(self):
        if 0 <= self.__rl_angle < 180:
            self.__rl_angle = self.__rl_angle - 10
        else:
            return
        self.__rl.ChangeDutyCycle(2.5 + 10*self.__rl_angle/180)
        time.sleep(0.02)
        self.__rl.ChangeDutyCycle(0)
        time.sleep(0.5)
        
    def left(self):
        if 0 < self.__rl_angle <= 180:
            self.__rl_angle = self.__rl_angle + 10
        else:
            return
        self.__rl.ChangeDutyCycle(2.5 + 10*self.__rl_angle/180)
        time.sleep(0.02)
        self.__rl.ChangeDutyCycle(0)
        time.sleep(0.5)
        
if __name__ == '__main__':
    clouldmon = Monitor()
    clouldmon.set_angle(145,100)
    while(True):
        clouldmon.right()
        time.sleep(0.5)
