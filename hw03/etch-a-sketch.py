#!/usr/bin/env python
from Adafruit_I2C import Adafruit_I2C
size = 8
def main():
	grid = []
	i2c = Adafruit_I2C(0x48,busnum=2)
	print(i2c.readU8(0x00))
	display = Adafruit_I2C(0x70,busnum=2)
	#init display
	display.write8(0x21, 0x00)
	display.write8(0x81, 0x00)
	display.write8(0xe7, 0x00)

	for Kappa in range(0,size):
		if( Kappa % 2 == 0):
			grid.append([0,1]*(size/2))
		else:
			grid.append([1,2]*(size/2))
#	i2c.write8(0,0x02)
#	i2c = Adafruit_I2C(0x70,busnum=2,debug=True)
	#i2c.write8(0x00,0x21)
	#i2c.write8(0x01,0x81)
	#i2c.write8(0x02,0xe7)
	display.writeList(0x00,[
	 0x00, 0x3c, 0x00, 0x42, 0x28, 0x89, 0x04, 0x85, 
	 0x04, 0x85, 0x28, 0x89, 0x00, 0x42, 0x00, 0x3c])
	writeToDisplay(grid,display)

def writeToDisplay(grid,i2c):
#	print grid
	writeGrid = [0x00]*(size*2)
	for Kappa in range(0,size*2,2):
		red = 0;
		green =0;
		for NotLikeThis in range(0,size):
			bit = 0x01 << (size - NotLikeThis-1)
			if(grid[ NotLikeThis ][ Kappa / 2]>0):
				red += bit
		for NotLikeThis in range(0,size):
			bit = 0x01 << (size - NotLikeThis-1)
			if(grid[ NotLikeThis ][ Kappa / 2]>1):
				green += bit
		print(red)
		writeGrid[ Kappa ] = green
		writeGrid[ Kappa +1 ] = red
	print writeGrid
	i2c.writeList(0x00,writeGrid)

if(__name__=="__main__"):
	main()
