import Adafruit_BBIO.GPIO as GPIO
import sys,os,time
import threading
running = True

state = [1,1,0,0]
outputs = ["P9_11","P9_13","P9_15","P9_17"]

def main():
    global running # other wise we cant stop thread
	#set up pins
    for out in outputs:
        GPIO.setup(out,GPIO.OUT)
        GPIO.output(out,GPIO.LOW)
    GPIO.output(outputs[0], GPIO.HIGH)
    GPIO.output(outputs[1], GPIO.HIGH)

	#start thread to run program
    thread = threading.Thread(target= lambda:function())
    thread.start()

    print("Enter anything to quit")
    raw_input() #stall program till user presses enter, 

    #clean up
    running = False
    for out in outputs:
        GPIO.output(out,GPIO.LOW)
    GPIO.cleanup()

def function():
	#thread function
    global state
    global outputs
    while running:
        print state 
        time.sleep(1)
        stepLeft()
    for out in outputs:
        GPIO.output(out,GPIO.LOW)

def stepLeft():
    global state
    global outputs
    ones =0
    for Kappa in state:
        ones += Kappa
    if(ones==2):
        removeLeft()
    else:
        addRight()

def removeLeft():
    if(state[ len(outputs)-1]==1 and state[0]==1):
        outPin = outputs[ len(outputs) -1 ]
        GPIO.output(outPin, GPIO.LOW)
        state[ len(outputs)-1 ]=0
        return
    for Kappa in range(0,len(outputs)):
        if(state[ Kappa ]==1):
            outPin = outputs[ Kappa ]
            GPIO.output(outPin, GPIO.LOW)
            state[ Kappa ]=0
            return

def addRight():
    for Kappa in range(0,len(outputs)):
        if(state[ Kappa ]==1):
            if(Kappa+1 == len(outputs)):
                outPin = outputs[ -Kappa-1 ]
                GPIO.output(outPin, GPIO.HIGH)
                state[- Kappa -1]=1
            else:
                outPin = outputs[ Kappa+1 ]
                GPIO.output(outPin, GPIO.HIGH)
                state[ Kappa +1]=1
            return 

def stepRight():
    global state
    global outputs
    ones =0
    for Kappa in state:
        ones += Kappa
    if(ones==1):
        for Kappa in range(0,len(outputs)):
            if(state[ Kappa ]==1):
                outPin = outputs[ Kappa -1]
                GPIO.output(outPin, GPIO.HIGH)
                state[ Kappa -1]=1
                return
    else:
        flag =1
        if(state[ len(outputs)-1]==1 and state[0]==1):
            outPin = outputs[ 0 ]
            GPIO.output(outPin, GPIO.LOW)
            state[ 0 ]=0
            return
        for Kappa in range(0,len(outputs)):
            if(state[ Kappa ]==1):
                if(flag):
                    flag = 0
                else:
                    outPin = outputs[ Kappa ]
                    GPIO.output(outPin, GPIO.LOW)
                    state[ Kappa ]=0
                    return 

if(__name__=="__main__"):
	main()
