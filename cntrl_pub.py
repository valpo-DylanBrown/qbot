#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
import RPi.GPIO as gpio
from datetime import datetime
from time import sleep, time

CH3 = 12
CH4 = 13
  
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

    if gpio.input(CH4):
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

    if gpio.input(CH3):
        #rising edge
        risingCount_vert += 1
        timeStart_vert = time()
    else:
        #falling edge
        if (risingCount_vert != 0):
            timePassed = time() - timeStart_vert
            #make pulseWidth an average
            pulseWidth_vert = ((pulseWidth_vert*(risingCount_vert-1)) + timePassed)/risingCount_vert

if __name__ == '__main__':
  rospy.init_node('ch_publisher')
  #rospy.init_node('ch4_publisher')
  ch3_pub = rospy.Publisher('ch3_state', Float32, queue_size=10)
  ch4_pub = rospy.Publisher('ch4_state', Float32, queue_size=10)
  gpio.setmode(gpio.BOARD)
  
  gpio.setup(CH3, gpio.IN)
  gpio.setup(CH4, gpio.IN)
  gpio.add_event_detect(CH4, gpio.BOTH, callback=edgeDetected_horiz)
  gpio.add_event_detect(CH3, gpio.BOTH, callback=edgeDetected_vert)
  #rate = rospy.Rate(100)
  
  while not rospy.is_shutdown():
    #rate.sleep()
    sleep(.1)
    dc_horiz = round(pulseWidth_horiz * risingCount_horiz * 100 * 10, 2)
    dc_vert = round(pulseWidth_vert * risingCount_vert * 100 * 10, 2)
    #print("DC VERT = {0}".format(dc_vert))
    ch3_pub.publish(dc_vert)
    ch4_pub.publish(dc_horiz)
    risingCount_horiz = 0
    risingCount_vert = 0
    pulseWidth_horiz = 0
    pulseWidth_vert = 0
    
    
    
  gpio.cleanup()

