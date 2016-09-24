#!/usr/bin/env python
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO

matrixAddr = 0x70
display = Adafruit_I2C(0x70,busnum=2)
sio = socketio.Server()
app = Flask(__name__)

#initial grid
size=8
grid = []
for i in range(0,size):
	grid.append([0]*size)

#the webpage handling
@app.route('/')
def index():
	return render_template('base.html')


#socket.io message handling
@sio.on('connect',namespace='/')
def connect(sid, environ):
	pass
	#print("Connected",environ)

@sio.on('matrix')
def matrix(sid,message):
    global matrixAddr
    addr = int(str(message),16)
    if(addr != matrixAddr):
        #use a new addr for the matrix
        matrixAddr = addr
        display = Adafruit_I2C(matrixAddr,busnum=2)
    #transmit the matrix grid
    sio.emit('matrix',grid)

@sio.on('brightness')
def brightness(sid,message):
    #sets the brightness
    display.write8(message['i'],0x00)


@sio.on('i2cset',namespace='/')
def setGrid(sid, message):
    #sets the collor on the display
	try:
		i = message['i']
		j = message['j']
		value = message['disp']
		grid[i][j] = value
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
    #starts the server
    display.write8(0x21, 0x00) #grid init calls
    display.write8(0x81, 0x00)
    display.write8(0xe7, 0x00)
    writeToDisplay(grid) #clear grid
    app = socketio.Middleware(sio,app) #wraps app in socket io handling
    eventlet.wsgi.server(eventlet.listen(('',8090)),app) #starts the server
