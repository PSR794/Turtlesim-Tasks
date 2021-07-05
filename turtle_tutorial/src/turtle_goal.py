#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def cb_goal(position): #call back function
    #updating the position of turtle in the turt_pose variable
    turt_pose.x=position.x
    turt_pose.y=position.y
    turt_pose.theta=position.theta
    turt_pose.linear_velocity=position.linear_velocity
    turt_pose.angular_velocity=position.angular_velocity
    
if __name__ == "__main__":
    try:
        #variable declarations
        global turt_pose,vel,tolerance
        vel=Twist()
        turt_pose=Pose()
        tolerance=0.01
        
        #user inputs
        x_goal=float(input('plz input goal x coordinate'))
        y_goal=float(input('plz input goal y coordinate'))
        
        #node initialization
        rospy.init_node("turtle_teleop",anonymous=True)
        goal_pub=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
        
        #setting the publishing rate
        rate=rospy.Rate(1)

        #subscribing the position
        rospy.Subscriber("/turtle1/pose", Pose, cb_goal)

        #loop for the locomotion
        while not rospy.is_shutdown():
            dist=( ((x_goal-turt_pose.x)**2) + ((y_goal-turt_pose.y)**2) )**0.5 
#            print(dist)
#            print(turt_pose)
#            print(vel)
            vel.linear.x=0.3*(dist) #using proportional controller for changing the linear and angular velocity
            vel.angular.z=1*(math.atan2((y_goal-turt_pose.y),(x_goal-turt_pose.x) )-turt_pose.theta)
            print(math.atan2((y_goal-turt_pose.y),(x_goal-turt_pose.x) ),turt_pose.theta) 
            goal_pub.publish(vel) #publishing the velocity
            rate.sleep()
            if dist<tolerance: 
                break           
    except rospy.ROSInterruptException:
        pass