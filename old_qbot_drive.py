#!/usr/bin/env python3

from __future__ import print_function

import threading
from std_msgs.msg import Float32
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

global ch1_movement
global ch2_movement
ch1_movement = 0
ch2_movement = 0

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

moveBindings = {
        'u':(1,0,0,1),
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        
        'm':(-1,0,0,-1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
       
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('RosAria/cmd_vel', Twist, queue_size = 1)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def run(self):
        twist = Twist()
        while not self.done:
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twist)

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist)


def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


# def vels(speed, turn):
    # return "currently:\tspeed %s\tturn %s " % (speed,turn)

def ch1_state_callback(msg):
    global ch1_movement
    if (msg.data > 10.5) or (msg.data < 4.5):
        return
    if msg.data > 8.5:
        ch1_movement = -1
    elif msg.data < 6.5:
        ch1_movement = 1
    else:
        ch1_movement = 0

def ch2_state_callback(msg):
    global ch2_movement
    if (msg.data > 10.5) or (msg.data < 4.5):
        return
    if msg.data > 8.5:
        ch2_movement = 1
    elif msg.data < 6.5:
        ch2_movement = -1
    else:
        ch2_movement = 0

if __name__=="__main__":
    #settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('qbot_drive')

    speed = rospy.get_param("~speed", 0.5)
    turn = rospy.get_param("~turn", 1.0)
    repeat = rospy.get_param("~repeat_rate", 0.0)
    key_timeout = rospy.get_param("~key_timeout", 0.0)
    if key_timeout == 0.0:
        key_timeout = None

    pub_thread = PublishThread(repeat)

    x = 0
    y = 0
    z = 0
    th = 0
    #status = 0
    rospy.Subscriber('ch1_state', Float32, ch1_state_callback)
    rospy.Subscriber('ch2_state', Float32, ch2_state_callback)
    loop = 1

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(x, y, z, th, speed, turn)

        #print(msg)
        #print(vels(speed,turn))

        
        while True:
            #key = getKey(key_timeout)
            x = ch2_movement
            y = 0
            z = 0
            if(x == -1):
                th = x * ch1_movement
            else:
                th = ch1_movement
            # if key in moveBindings.keys():
                # x = moveBindings[key][0]
                # y = moveBindings[key][1]
                # z = moveBindings[key][2]
                # th = moveBindings[key][3]
            #elif key in speedBindings.keys():
                #speed = speed * speedBindings[key][0]
                #turn = turn * speedBindings[key][1]

                #print(vels(speed,turn))
                #if (status == 14):
                    #print(msg)
                #status = (status + 1) % 15
            # else:
                # # Skip updating cmd_vel if key timeout and robot already
                # # stopped.
                # if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    # continue
                # x = 0
                # y = 0
                # z = 0
                # th = 0
                # if (key == '\x03'):
                    # break
            pub_thread.update(x, y, z, th, speed, turn)
    except KeyboardInterrupt:
        print("User requested stop")
        
    except Exception as e:
        print(e)
    finally:
        pub_thread.stop()

        #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
