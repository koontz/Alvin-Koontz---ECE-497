#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import sys,os,time
import threading
running = True

def main():
	global running # other wise we cant stop thread
	out = "P9_27"
	input = "P9_26"

	GPIO.setup(out,GPIO.OUT)
	GPIO.output(out,GPIO.HIGH)
	GPIO.setup(input,GPIO.IN)
	GPIO.add_event_detect(input,GPIO.FALLING)#sets a flag on the pin

	#start thread to monitor inputs
	thread = threading.Thread(target= lambda:switchOnFall(input,out))
	thread.start()

	print("Enter anything to quit")
	raw_input() #stall program till user presses enter, 

	#clean up
	running = False
	GPIO.output(out,GPIO.LOW)
	GPIO.cleanup()

def switchOnFall(inPin,outPin):
	#thread function
    while running:
		#GPIO.wait_for_edge(inPin,GPIO.FALLING) #blocking call
		#if(GPIO.event_detected(inPin)): #polls the flag
		#	GPIO.output(outPin, 1 ^ GPIO.input(outPin))
		#	event = True

#        GPIO.wait_for_edge(inPin, GPIO.FALLING)
        if(GPIO.input(inPin)):
            GPIO.output(outPin,GPIO.HIGH)
        else:
            GPIO.output(outPin,GPIO.LOW)
#        time.sleep(0.1) # debouncing time frame

if(__name__=="__main__"):
	main()
