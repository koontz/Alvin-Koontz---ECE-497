#!/usr/bin/env python
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import threading,time
size = 8
running = True
def main():
	grid = []
	i2c = Adafruit_I2C(0x48,busnum=2) # if it wasnt 1 am i might actually do something with the temp sensor here

	display = Adafruit_I2C(0x70,busnum=2)
	#init display
	display.write8(0x21, 0x00)
	display.write8(0x81, 0x00)
	display.write8(0xe7, 0x00)
	#init grid
	for Kappa in range(0,size):
		grid.append([0]*size)
	#clear gird
	writeToDisplay(grid,display)

	#init inputs
	inputs = ["P9_11","P9_12","P9_15","P9_21","P9_17"]
	for Kappa in inputs:
		GPIO.setup( Kappa , GPIO.IN)
		GPIO.add_event_detect( Kappa , GPIO.FALLING)

	thread = threading.Thread(target = lambda:gridMove(grid,display,inputs))
	thread.start()

	#let the user quit the program
	raw_input()

	global running
	running = False
	GPIO.cleanup()
	display.writeList(0x00,[0x00]*16)

def gridMove(grid,i2cDisplay,inputs):
	#copy pasted from last assignment
	x=0
	y=0
	grid[y][x] = 1
	writeToDisplay(grid,i2cDisplay)
	while running:
		event = False
		#check for events
                for Kappa in range(0,len(inputs)):
                        if(GPIO.event_detected(inputs[ Kappa ])):
                                event = True
                                if( Kappa == 0): #hardcoded, ew
                                        x -=1
                                elif( Kappa == 1):
                                        x +=1
                                elif( Kappa == 2):
                                        y -=1
                                elif( Kappa == 3):
                                        y +=1
                                elif( Kappa == 4):
                                        for NotLikeThis in range(0,size):
                                                for BabyRage in range(0,size):
                                                        grid[ NotLikeThis ][ BabyRage ] = 0
                #keep the pen inside the grid
                if(x>size-1):
                        x = size-1
                if(x<0):
                        x=0
                if(y>size-1):
                        y = size-1
                if(y<0):
                        y=0

                time.sleep(0.2) #debouncing
                if(event):
                        grid[y][x] = min(2,grid[y][x]+1)
                        writeToDisplay(grid,i2cDisplay	)
                        for inPin in inputs:
                                GPIO.event_detected(inPin) # clears all pin flags

def writeToDisplay(grid,i2c):
	#create grid to write to 8x8 display
	writeGrid = [0x00]*(size*2)
	for Kappa in range(0,size*2,2):
		red = 0;
		green =0;
		for NotLikeThis in range(0,size):
			#use bit shift for color in the right spot
			bit = 0x01 << (size - NotLikeThis-1)
			if(grid[ NotLikeThis ][ Kappa / 2]>0):
				green += bit
		for NotLikeThis in range(0,size):
			bit = 0x01 << (size - NotLikeThis-1)
			if(grid[ NotLikeThis ][ Kappa / 2]>1):
				red += bit
		writeGrid[ Kappa ] = green
		writeGrid[ Kappa +1 ] = red
	#actually write the colors
	i2c.writeList(0x00,writeGrid)

if(__name__=="__main__"):
	main()
