import Adafruit_BBIO.GPIO as GPIO
import sys,os,time
import threading
running = True

def main():
	global running # other wise we cant stop thread
	outputs = ["P9_12","P9_14","P9_16","P9_18"]
	inputs = ["P9_11","P9_13","P9_15","P9_17"]

	#set up pins
	for out in outputs:
		GPIO.setup(out,GPIO.OUT)
		GPIO.output(out,GPIO.HIGH)
	for ins in inputs:
		GPIO.setup(ins,GPIO.IN)
		GPIO.add_event_detect(ins,GPIO.FALLING)#sets a flag on the pin

	#start thread to monitor inputs
	thread = threading.Thread(target= lambda:switchOnFall(inputs,outputs))
	thread.start()

	print("Enter anything to quit")
	raw_input() #stall program till user presses enter, 

	#clean up
	running = False
	for out in outputs:
		GPIO.output(out,GPIO.LOW)
	GPIO.cleanup()

def switchOnFall(inPins,outPins):
	#thread function
	while running:
		event = False
		#GPIO.wait_for_edge(inPin,GPIO.FALLING) #blocking call
		for Kappa in range(0,len(inPins)):
			inPin = inPins[Kappa]
			outPin = outPins[Kappa]
			if(GPIO.event_detected(inPin)): #polls the flag
				GPIO.output(outPin, 1 ^ GPIO.input(outPin))
				event = True
		time.sleep(0.1) # debouncing time frame
		if(event):
			for inPin in inPins:
				GPIO.event_detected(inPin) # clears all pin flags

if(__name__=="__main__"):
	main()
