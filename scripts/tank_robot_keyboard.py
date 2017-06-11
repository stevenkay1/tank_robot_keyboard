#!/usr/bin/env python
import roslib
import rospy

import math

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
w - forward
s - reverse
a - point turn left
d - point turn right


Speed Control:
q - +0.1
e - -0.1


anything else : stop


CTRL-C to quit
"""

moveBindings = {
		# Forward
		'w':(1,0,0,0),
		# Backward
		'd':(0,0,0,1),
		# Skid Steer Right
		'a':(0,0,0,-1),
		# Skid Steer Left
		's':(-1,0,0,0),

	       }

speedBindings={
		'q':(0.1,0.1),
		'e':(-0.1,-0.1),
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	rospy.init_node('tank_robot_keyboard')

	speed = rospy.get_param("~speed", 0.0)
	turn = rospy.get_param("~turn", 0.0)
	x = 0
	y = 0
	z = 0
	th = 0
	status = 0

	try:
		print msg
		print vels(speed,turn)
		while(1):
			key = getKey()
			if key in moveBindings.keys():
				x = moveBindings[key][0]
				y = moveBindings[key][1]
				z = moveBindings[key][2]
				th = moveBindings[key][3]

			elif key in speedBindings.keys():
				speed = speed + speedBindings[key][0]
				turn = turn + speedBindings[key][1]

				if speed < 0.01:
					speed = 0.0

				if turn < 0.01:
					turn = 0.0


				print vels(speed,turn)
				if (status == 14):
					print msg
				status = (status + 1) % 15
			else:
				x = 0
				y = 0
				z = 0
				th = 0
				if (key == '\x03'):
					break

			twist = Twist()

			twist.linear.x = x* abs(speed)
			twist.angular.z = th*abs(turn)

			# unused
			twist.linear.y = 0
			twist.linear.z = 0
			twist.angular.x = 0
			twist.angular.y = 0


			pub.publish(twist)

	except:
		print e

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


