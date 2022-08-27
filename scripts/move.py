#!/usr/bin/env python3

import cmd
from dis import dis
from re import X
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math 
import time


x=0
y=0
yaw=0


def poseCallback(pose_message):
    global x
    global y
    global yaw
    x=pose_message.x
    y=pose_message.y
    yaw=pose_message.theta


def go_to_goal():
    global x
    global y
    global yaw
    xg,yg=int(input("Enter Value of x: ")),int(input("Enter Value of y: "))
    
    velocity_message=Twist()
    cmd_vel_topic="/turtle1/cmd_vel"
    while(True):
        k_linear=0.5
        distance=abs(math.sqrt(((x-xg)**2)+((y-yg)**2)))

        linear_speed=k_linear*distance

        k_angular=4
        desired_angle_goal=math.atan2(yg-y,xg-x)
        angular_speed=(desired_angle_goal-yaw)*k_angular

        velocity_message.linear.x=linear_speed
        velocity_message.angular.z=angular_speed

        velocity_publisher.publish(velocity_message)
      
        if(distance<0.01):
            go_to_goal()

    

if __name__=="__main__":
    rospy.init_node("turtlesim_motion_pose",anonymous=True)

    cmd_vel_topic="/turtle1/cmd_vel"
    velocity_publisher=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)

    position_topic="/turtle1/pose"
    pose_subscriber=rospy.Subscriber(position_topic,Pose,poseCallback)
    time.sleep(2)
    go_to_goal()
