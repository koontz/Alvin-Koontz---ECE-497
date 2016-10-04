#!/usr/bin/env python
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import sys, subprocess, json, time
import urllib2

def main():
    #creates the i2c connections
    tmp1 = Adafruit_I2C(0x48,busnum=2)
    tmp2 = Adafruit_I2C(0x4a,busnum=2)
    output = open('data.json', 'w')
    data = {}
    #read 120 points of data
    for i in range(0,120):
        point = (tmp1.readU8(0x00) , tmp2.readU8(0x00))
        data[i] = point
        print point
        time.sleep(1)
    #save the data to data.json
    json.dump(data,output)
    output.close()
    #read data
    data = json.load(open('data.json'))
    keys = json.load(open('keys_tmp101.json'))
    #generate post url
    url = keys['inputUrl'] + "/?private_key=" + keys['privateKey'] + "&temp1={}&temp2={}"
    #post the read in data
    for i in range(0,120):
        try:
            point = data['{}'.format(i)]
            request = url.format(point[0],point[1])
            #print point
            #print(request , urllib2.urlopen(request).read())
            time.sleep(1) #the server lag actualy makes it hard to post data at 1 sample per second more work would be needed to handle it
        except:
            pass #server error
            #not sure what to do about this, commonly get a 503 error so best just to skip the point 


if(__name__=="__main__"):
	main()
