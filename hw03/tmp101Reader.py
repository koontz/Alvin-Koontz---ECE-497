#!/usr/bin/env python
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import sys, subprocess

def main():
	#input the pin that the alert signal is fed into
	input = "P9_13"
	triggerLevel = 0x19 #25C or 77F
	GPIO.setup(input,GPIO.IN)
	tmp1 = Adafruit_I2C(0x48,busnum=2)
	tmp2 = Adafruit_I2C(0x4a,busnum=2)

	#set the values of the registers to enable alert pin
	tmp1.write8(0x01,0x00)	#sets alert flag to be in comapare mode, active low 
	tmp2.write8(0x01,0x00)	#sets alert flag to be in comapare mode, active low 
	tmp1.write8(0x02,triggerLevel)
	tmp1.write8(0x03,triggerLevel)
	tmp2.write8(0x02,triggerLevel)
	tmp2.write8(0x03,triggerLevel)


	ALERT_ALERT = GPIO.input(input)#check if we alert has allready happend
	if(not ALERT_ALERT):
		subprocess.call(['./readTMP.sh'])
		sys.exit(1)

	GPIO.wait_for_edge(input, GPIO.FALLING) #technically this call waits for an interupt

	subprocess.call(['./readTMP.sh'])
	

if(__name__=="__main__"):
	main()
