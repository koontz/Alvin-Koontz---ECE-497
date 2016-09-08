import sys, getopt
import Adafruit_BBIO.GPIO as GPIO
import sys,os,time
import threading
import curses

#globals
running = True

def main():
	global running
	global stdscr
	sizeX = 0
	sizeY = 0
	inputs = ["P9_11","P9_13","P9_15","P9_17","P9_18"]

	while(sizeY <=0 or sizeY > 100):
		print("Please enter vaild grid height")
		try:
			sizeY = int(raw_input()) 
		except:
			pass
	while(sizeX <=0 or sizeX > 100):
		print("Please enter vaild grid width")
		try:
			sizeX = int(raw_input()) 
		except:
			pass
	output = []
	print('Size {} x {}'.format(sizeX,sizeY))
	print("Press enter to start")
	raw_input()
	stdscr = curses.initscr()
	

	for s in range(0,sizeY):
		row = [False]*sizeX
		output.append(row)
	for ins in inputs:
		GPIO.setup(ins,GPIO.IN)
		GPIO.add_event_detect(ins,GPIO.FALLING) #sets a flag on the pin

	thread = threading.Thread(target= lambda:moveOnGrid(output,inputs,sizeX,sizeY))
        thread.start()

	stdscr.getch()

	curses.endwin()
	running = False
	GPIO.cleanup()


def moveOnGrid(grid,inputs,sizeX,sizeY):
	x = 0
	y = 0
	grid[y][x] = True
	printGrid(grid)
	while running:
		event = False
		for Kappa in range(0,len(inputs)):
			if(GPIO.event_detected(inputs[Kappa])):
				event = True
				if(Kappa == 0): #hardcoded, ew
					x -=1
				elif(Kappa == 1):
					x +=1
				elif(Kappa == 2):
					y -=1
				elif(Kappa == 3):
					y +=1
				elif(Kappa == 4):
					for NotLikeThis in range(0,len(grid)):
						for BabyRage in range(0,len(grid[0])):
							grid[NotLikeThis][BabyRage] = False
		if(x>sizeX-1):
	        	x = sizeX-1
		if(x<0):
                	x=0
                if(y>sizeY-1):
                	y = sizeY-1
	        if(y<0):
			y=0

		time.sleep(0.2) #debouncing
		if(event):
			grid[y][x] = True
			printGrid(grid)
			for inPin in inputs:
				GPIO.event_detected(inPin) # clears all pin flags

#format the output
def printGrid(grid):
	printString = ""
	top = "    " 
	for i in range(0,len(grid[0])):
		top += str(i)+" "
		if(i<10):
			top+=" "
#	stdscr.addstr(0,0,top)
#	print(top)
	printString = top
	for i in range(len(grid)):
		row = str(i)+": "
		if(i<10):
			row+=" "
		for col in grid[i]:
			if col:
				row+='X  '
			else:
				row+='   '
#		print(row)
#		stdscr.addstr(row)
		printString += "\n" + row
#	print(printString)
	stdscr.addstr(0,0,printString)
	stdscr.refresh()

if __name__ == '__main__':
	main()
