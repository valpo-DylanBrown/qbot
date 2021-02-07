import RPi.GPIO as gpio
from datetime import datetime
from time import sleep, time



gpio.setmode(gpio.BOARD)
gpio.setup(32, gpio.IN)
gpio.setup(8, gpio.OUT)
gpio.setup(10, gpio.OUT)
gpio.setup(12, gpio.IN)
gpio.setup(3, gpio.OUT)
gpio.setup(5, gpio.OUT)

global risingCount_horiz
global pulseWidth_horiz
global timeStart_horiz
risingCount_horiz = 0
pulseWidth_horiz=0
timeStart_horiz=0

global risingCount_vert
global pulseWidth_vert
global timeStart_vert
risingCount_vert = 0
pulseWidth_vert=0
timeStart_vert=0

def edgeDetected_horiz(channel):

    global risingCount_horiz
    global pulseWidth_horiz
    global timeStart_horiz

    if gpio.input(32):
        #rising edge
        risingCount_horiz += 1
        timeStart_horiz = time()
    else:
        #falling edge
        if (risingCount_horiz != 0):
            timePassed = time() - timeStart_horiz
            #make pulseWidth an average
            pulseWidth_horiz = ((pulseWidth_horiz*(risingCount_horiz-1)) + timePassed)/risingCount_horiz

def edgeDetected_vert(channel):

    global risingCount_vert
    global pulseWidth_vert
    global timeStart_vert

    if gpio.input(12):
        #rising edge
        risingCount_vert += 1
        timeStart_vert = time()
    else:
        #falling edge
        if (risingCount_vert != 0):
            timePassed = time() - timeStart_vert
            #make pulseWidth an average
            pulseWidth_vert = ((pulseWidth_vert*(risingCount_vert-1)) + timePassed)/risingCount_vert

gpio.add_event_detect(32, gpio.BOTH, callback=edgeDetected_horiz)
gpio.add_event_detect(12, gpio.BOTH, callback=edgeDetected_vert)

try:
	while True:
		sleep(.1)
		dc_horiz = round(pulseWidth_horiz * risingCount_horiz * 100 * 10, 2)
		dc_vert = round(pulseWidth_vert * risingCount_vert * 100 * 10, 2)
		print("DC HORIZ = {0}, DC VERT = {1}".format(dc_horiz, dc_vert))
		if dc_horiz > 8.5:
			gpio.output(8, gpio.LOW)
			gpio.output(10, gpio.HIGH)
		elif dc_horiz < 6.5:
			gpio.output(10, gpio.LOW)
			gpio.output(8, gpio.HIGH)
		else:
			gpio.output(10, gpio.LOW)
			gpio.output(8, gpio.LOW)
		if dc_vert > 8.5:
			gpio.output(5, gpio.LOW)
			gpio.output(3, gpio.HIGH)
		elif dc_vert < 6.5:
			gpio.output(3, gpio.LOW)
			gpio.output(5, gpio.HIGH)
		else:
			gpio.output(3, gpio.LOW)
			gpio.output(5, gpio.LOW)
		#print("PWM = {0}hz, dutyCycle = {1}%".format(risingCount, round(pulseWidth * risingCount * 100,2)))
		risingCount_horiz = 0
		risingCount_vert = 0
		pulseWidth_horiz = 0
		pulseWidth_vert = 0

except KeyboardInterrupt:
	
	print("quit")
	gpio.cleanup()
