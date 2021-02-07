#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
import RPi.GPIO as gpio
UP_LED = 5
DOWN_LED = 40
LEFT_LED = 10
RIGHT_LED = 8
def ch3_state_callback(msg):
    if msg.data > 8.5:
      gpio.output(DOWN_LED, gpio.LOW)
      gpio.output(UP_LED, gpio.HIGH)
    elif msg.data < 6.5:
      gpio.output(UP_LED, gpio.LOW)
      gpio.output(DOWN_LED, gpio.HIGH)
    else:
      gpio.output(UP_LED, gpio.LOW)
      gpio.output(DOWN_LED, gpio.LOW)
def ch4_state_callback(msg):
    if msg.data > 8.5:
      gpio.output(LEFT_LED, gpio.LOW)
      gpio.output(RIGHT_LED, gpio.HIGH)
    elif msg.data < 6.5:
      gpio.output(RIGHT_LED, gpio.LOW)
      gpio.output(LEFT_LED, gpio.HIGH)
    else:
      gpio.output(RIGHT_LED, gpio.LOW)
      gpio.output(LEFT_LED, gpio.LOW)
if __name__ == '__main__':
    rospy.init_node('led_sub')
    gpio.setmode(gpio.BOARD)
    gpio.setup(UP_LED, gpio.OUT)
    gpio.setup(DOWN_LED, gpio.OUT)
    gpio.setup(LEFT_LED, gpio.OUT)
    gpio.setup(RIGHT_LED, gpio.OUT)
    rospy.Subscriber('ch3_state', Float32, ch3_state_callback)
    rospy.Subscriber('ch4_state', Float32, ch4_state_callback)
    rospy.spin()
    gpio.cleanup()