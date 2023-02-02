#!/usr/bin/env python3

import rospy
# Import Twist Messages
from geometry_msgs.msg import Twist
# Import turtlesim pose message
from turtlesim.msg import Pose
# Import the Turtlecontrol message
from robotics_lab1.msg import Turtlecontrol
# Might need this
import math

vel_cmd = Twist()
Turtle_Position = Pose()
Control_Info = Turtlecontrol()

def turtleBot_position(data):
	global Turtle_Position
	Turtle_Position.x = data.x

def user_control_params(data):
	global Control_Info
	Control_Info.kp = data.kp
	Control_Info.xd = data.xd
	
def proportional_control(Turtle_Pos_X, Control_kp, Control_xd):
	global vel_cmd
	#error = Control_xd - Turtle_Pos_X
	#new_velocity = Control_kp * error
	
	new_velocity = Control_kp*(Control_xd - Turtle_Pos_X)
	
	vel_cmd.linear.x = new_velocity


if __name__ == '__main__':
	# initialize the node
	rospy.init_node('control_node', anonymous = True)
	
	# Subscribe to the pose topic and send the pose information to the proportional_control function
	rospy.Subscriber('/turtle1/pose', Pose, turtleBot_position)
	
	# Subscribe to the control parameter topic
	rospy.Subscriber('/turtle1/control_params', Turtlecontrol, user_control_params)
	
	# Set up Publisher for cmd_vel to send new linear velocity to?
	pos_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
	
	# Set a 10Hz frequency for the loop
	loop_rate = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		
		proportional_control(Turtle_Position.x, Control_Info.kp,Control_Info.xd)
		pos_pub.publish(vel_cmd)
	
		loop_rate.sleep()
