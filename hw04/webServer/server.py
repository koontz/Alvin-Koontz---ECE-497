#!/usr/bin/env python
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO

display = Adafruit_I2C(0x70,busnum=2)
sio = socketio.Server()
app = Flask(__name__)

size=8
grid = []
for i in range(0,size):
	grid.append([0]*size)
print grid

@app.route('/')
def index():
	return render_template('base.html')

@sio.on('connect',namespace='/')
def connect(sid, environ):
	print("Connected",environ)

@sio.on('i2cset',namespace='/')
def setGrid(sid, message):
	try:
		i = message['i']
		j = message['j']
		value = message['disp']
		grid[j][i] = value
		writeToDisplay(grid)
	except:
		pass

def writeToDisplay(grid):
        #create grid to write to display
        writeGrid = [0x00]*(size*2)
        for Kappa in range(0,size*2,2):
                red = 0;
                green =0;
                for NotLikeThis in range(0,size):
                        #use bit shift for color in the right spot
                        bit = 0x01 << (size - NotLikeThis-1)
                        if(grid[ NotLikeThis ][ Kappa / 2]>0 and grid[ NotLikeThis ][ Kappa / 2]<3):
                                green += bit
                for NotLikeThis in range(0,size):
                        bit = 0x01 << (size - NotLikeThis-1)
                        if(grid[ NotLikeThis ][ Kappa / 2]>1):
                                red += bit
                writeGrid[ Kappa ] = green
                writeGrid[ Kappa +1 ] = red
        #actually write the colors
        display.writeList(0x00,writeGrid)


if(__name__ == "__main__"):
	writeToDisplay(grid)
	display.write8(0x21, 0x00)
        display.write8(0x81, 0x00)
        display.write8(0xe7, 0x00)
	app = socketio.Middleware(sio,app)
	eventlet.wsgi.server(eventlet.listen(('',8090)),app)
