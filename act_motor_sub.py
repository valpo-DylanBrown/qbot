#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
import RPi.GPIO as gpio
LG_ACT_EXTEND = 5
LG_ACT_RETRACT = 40
SM_ACT_EXTEND = 10
SM_ACT_RETRACT = 8
MOTOR_ENA1 = 38
MOTOR_ON = 11
MOTOR_OFF = 15
def ch3_state_callback(msg):
    if msg.data > 8.5:
      gpio.output(LG_ACT_RETRACT, gpio.LOW)
      gpio.output(LG_ACT_EXTEND, gpio.HIGH)
    elif msg.data < 6.5:
      gpio.output(LG_ACT_EXTEND, gpio.LOW)
      gpio.output(LG_ACT_RETRACT, gpio.HIGH)
    else:
      gpio.output(LG_ACT_EXTEND, gpio.LOW)
      gpio.output(LG_ACT_RETRACT, gpio.LOW)
def ch4_state_callback(msg):
    if msg.data > 8.5:
      gpio.output(SM_ACT_EXTEND, gpio.LOW)
      gpio.output(SM_ACT_RETRACT, gpio.HIGH)
    elif msg.data < 6.5:
      gpio.output(SM_ACT_RETRACT, gpio.LOW)
      gpio.output(SM_ACT_EXTEND, gpio.HIGH)
    else:
      gpio.output(SM_ACT_RETRACT, gpio.LOW)
      gpio.output(SM_ACT_EXTEND, gpio.LOW)
def ch5_state_callback(msg):
    if msg.data > 8.5:
      gpio.output(MOTOR_ENA1, gpio.HIGH)
      gpio.output(MOTOR_OFF, gpio.LOW)
      gpio.output(MOTOR_ON, gpio.HIGH)
    elif msg.data < 6.5:
      gpio.output(MOTOR_ENA1, gpio.HIGH)
      gpio.output(MOTOR_ON, gpio.LOW)
      gpio.output(MOTOR_OFF, gpio.HIGH)
    else:
      gpio.output(MOTOR_ENA1, gpio.LOW)
      gpio.output(MOTOR_OFF, gpio.LOW)
      gpio.output(MOTOR_ON, gpio.LOW)
if __name__ == '__main__':
    rospy.init_node('actuator_motor_subscriber')
    gpio.setmode(gpio.BOARD)
    gpio.setup(LG_ACT_EXTEND, gpio.OUT)
    gpio.setup(LG_ACT_RETRACT, gpio.OUT)
    gpio.setup(SM_ACT_EXTEND, gpio.OUT)
    gpio.setup(SM_ACT_RETRACT, gpio.OUT)
    gpio.setup(MOTOR_ENA1, gpio.OUT)
    gpio.setup(MOTOR_OFF, gpio.OUT)
    gpio.setup(MOTOR_ON, gpio.OUT)
    rospy.Subscriber('ch3_state', Float32, ch3_state_callback)
    rospy.Subscriber('ch4_state', Float32, ch4_state_callback)
    rospy.Subscriber('ch5_state', Float32, ch5_state_callback)
    rospy.spin()
    gpio.cleanup()
