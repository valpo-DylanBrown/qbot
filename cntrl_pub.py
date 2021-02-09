#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
import RPi.GPIO as gpio
from datetime import datetime
from time import sleep, time

CH1 = 3
CH2 = 7
CH3 = 12
CH4 = 13
CH5 = 16

global ch1_risingCount
global ch1_pulseWidth
global ch1_timeStart
ch1_risingCount = 0
ch1_pulseWidth=0
ch1_timeStart=0

global ch2_risingCount
global ch2_pulseWidth
global ch2_timeStart
ch2_risingCount = 0
ch2_pulseWidth=0
ch2_timeStart=0
  
global ch4_risingCount
global ch4_pulseWidth
global ch4_timeStart
ch4_risingCount = 0
ch4_pulseWidth=0
ch4_timeStart=0

global ch3_risingCount
global ch3_pulseWidth
global ch3_timeStart
ch3_risingCount = 0
ch3_pulseWidth=0
ch3_timeStart=0

global ch5_risingCount
global ch5_pulseWidth
global ch5_timeStart
ch5_risingCount = 0
ch5_pulseWidth=0
ch5_timeStart=0

def ch1_edgeDetected(channel):

    global ch1_risingCount
    global ch1_pulseWidth
    global ch1_timeStart

    if gpio.input(CH1):
        #rising edge
        ch1_risingCount += 1
        ch1_timeStart = time()
    else:
        #falling edge
        if (ch1_risingCount != 0):
            timePassed = time() - ch1_timeStart
            #make pulseWidth an average
            ch1_pulseWidth = ((ch1_pulseWidth*(ch1_risingCount-1)) + timePassed)/ch1_risingCount

def ch2_edgeDetected(channel):

    global ch2_risingCount
    global ch2_pulseWidth
    global ch2_timeStart

    if gpio.input(CH2):
        #rising edge
        ch2_risingCount += 1
        ch2_timeStart = time()
    else:
        #falling edge
        if (ch2_risingCount != 0):
            timePassed = time() - ch2_timeStart
            #make pulseWidth an average
            ch2_pulseWidth = ((ch2_pulseWidth*(ch2_risingCount-1)) + timePassed)/ch2_risingCount

def ch4_edgeDetected(channel):

    global ch4_risingCount
    global ch4_pulseWidth
    global ch4_timeStart

    if gpio.input(CH4):
        #rising edge
        ch4_risingCount += 1
        ch4_timeStart = time()
    else:
        #falling edge
        if (ch4_risingCount != 0):
            timePassed = time() - ch4_timeStart
            #make pulseWidth an average
            ch4_pulseWidth = ((ch4_pulseWidth*(ch4_risingCount-1)) + timePassed)/ch4_risingCount

def ch3_edgeDetected(channel):

    global ch3_risingCount
    global ch3_pulseWidth
    global ch3_timeStart

    if gpio.input(CH3):
        #rising edge
        ch3_risingCount += 1
        ch3_timeStart = time()
    else:
        #falling edge
        if (ch3_risingCount != 0):
            timePassed = time() - ch3_timeStart
            #make pulseWidth an average
            ch3_pulseWidth = ((ch3_pulseWidth*(ch3_risingCount-1)) + timePassed)/ch3_risingCount
            
def ch5_edgeDetected(channel):

    global ch5_risingCount
    global ch5_pulseWidth
    global ch5_timeStart

    if gpio.input(CH5):
        #rising edge
        ch5_risingCount += 1
        ch5_timeStart = time()
    else:
        #falling edge
        if (ch5_risingCount != 0):
            timePassed = time() - ch3_timeStart
            #make pulseWidth an average
            ch5_pulseWidth = ((ch5_pulseWidth*(ch5_risingCount-1)) + timePassed)/ch5_risingCount

if __name__ == '__main__':
  rospy.init_node('ch_publisher')
  ch1_pub = rospy.Publisher('ch1_state', Float32, queue_size=10)
  ch2_pub = rospy.Publisher('ch2_state', Float32, queue_size=10)
  ch3_pub = rospy.Publisher('ch3_state', Float32, queue_size=10)
  ch4_pub = rospy.Publisher('ch4_state', Float32, queue_size=10)
  ch5_pub = rospy.Publisher('ch5_state', Float32, queue_size=10)
  gpio.setmode(gpio.BOARD)
  
  gpio.setup(CH1, gpio.IN)
  gpio.setup(CH2, gpio.IN)
  gpio.setup(CH3, gpio.IN)
  gpio.setup(CH4, gpio.IN)
  gpio.setup(CH5, gpio.IN)
  gpio.add_event_detect(CH1, gpio.BOTH, callback=ch1_edgeDetected)
  gpio.add_event_detect(CH2, gpio.BOTH, callback=ch2_edgeDetected)
  gpio.add_event_detect(CH4, gpio.BOTH, callback=ch4_edgeDetected)
  gpio.add_event_detect(CH3, gpio.BOTH, callback=ch3_edgeDetected)
  gpio.add_event_detect(CH5, gpio.BOTH, callback=ch5_edgeDetected)
  #rate = rospy.Rate(100)
  
  while not rospy.is_shutdown():
    #rate.sleep()
    sleep(.1)
    ch1_dutycycle = round(ch1_pulseWidth * ch1_risingCount * 100 * 10, 2)
    ch2_dutycycle = round(ch2_pulseWidth * ch2_risingCount * 100 * 10, 2)
    ch4_dutycycle = round(ch4_pulseWidth * ch4_risingCount * 100 * 10, 2)
    ch3_dutycycle = round(ch3_pulseWidth * ch3_risingCount * 100 * 10, 2)
    ch5_dutycycle = round(ch5_pulseWidth * ch5_risingCount * 100 * 10, 2)
    #print("DC VERT = {0}".format(dc_vert))
    ch1_pub.publish(ch1_dutycycle)
    ch2_pub.publish(ch2_dutycycle)
    ch3_pub.publish(ch3_dutycycle)
    ch4_pub.publish(ch4_dutycycle)
    ch5_pub.publish(ch5_dutycycle)
    ch1_risingCount = 0
    ch2_risingCount = 0
    ch4_risingCount = 0
    ch3_risingCount = 0
    ch5_risingCount = 0
    ch1_pulseWidth = 0
    ch2_pulseWidth = 0
    ch4_pulseWidth = 0
    ch3_pulseWidth = 0
    ch5_pulseWidth = 0
    
  gpio.cleanup()

