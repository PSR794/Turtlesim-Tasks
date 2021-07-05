#!/usr/bin/env python

import rospy 
from geometry_msgs.msg import Twist #for cmd_vel
from turtlesim.msg import Pose #for position 

def cb(Pose_msg):  #the callback function
  rospy.loginfo("POSITION\nX:%2f\nY:%2f\nANGLE:%2f\nV:%2f\nOMEGA:%2f\n",Pose_msg.x,Pose_msg.y,Pose_msg.theta,Pose_msg.linear_velocity,Pose_msg.angular_velocity)

if __name__ == "__main__":
  try:
    Vx=float(input('enter speed')) #user inputs
    wz=float(input('enter angular vel'))
    #initializing the node
    rospy.init_node('teleop_turtle', anonymous=True)
    #declaring publisher and subscriber
    tpub=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    tsub=rospy.Subscriber('/turtle1/pose', Pose, cb)
    #assigning values of cmd_vel
    vel=Twist()
    vel.linear.x=Vx
    vel.angular.z=wz
    rate=rospy.Rate(1)

    while not rospy.is_shutdown():
      #publishing the velocity
      tpub.publish(vel)
#      rospy.loginfo("CMD_VEL\n%2f\n%2f\n%2f\n%2f\n%2f\n%2f\n"vel.linear.x)
#      print(vel)     
      rate.sleep()

  except rospy.ROSInterruptException:
    pass