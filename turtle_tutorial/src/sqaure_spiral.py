#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def cb(pose_data):
#    print('hello')
    msg_p.x=pose_data.x
    msg_p.y=pose_data.y
    msg_p.theta=pose_data.theta
    msg_p.linear_velocity=pose_data.linear_velocity
    msg_p.angular_velocity=pose_data.angular_velocity
#    print(msg_p)

def start_point_PID(x,y,z):
    rate=rospy.Rate(1)
    w=tolerance

#    print('ho')
#    rate=rospy.Rate(1)
#    print('yo')
    while True:
#        print('while1')           
        d=( ((x - msg_p.x)**2) + ((y - msg_p.y)**2) )**0.5
        msg_v.linear.x=0.3*d
        if z==1:
            msg_v.angular.z=1*(math.atan2((y - msg_p.y), (x - msg_p.x))- msg_p.theta)
        elif z==4:
            msg_v.angular.z=0.4*(math.atan2((y - msg_p.y), (x - msg_p.x))- msg_p.theta)
        else:
            msg_v.angular.z=0
        spiral_pub.publish(msg_v)
        rate.sleep()

#        if z==4:
#            w=0.5
#        print(msg_p)
        if d<w:
            break
    
           
def turn(X,Y):
    while True:
        msg_v.linear.x=0
        dtheta=(math.atan2((Y - msg_p.y), (X - msg_p.x))- msg_p.theta)
        msg_v.angular.z=1*(math.atan2((Y - msg_p.y), (X - msg_p.x))- msg_p.theta)
        spiral_pub.publish(msg_v)
#        rate.sleep()
        if abs(dtheta)<(tolerance*0.001):
            break



if __name__ == '__main__':
    try:
        global msg_p, msg_v, tolerance, diff
#        print('hi')
        msg_p=Pose()
        msg_v=Twist()
        tolerance=0.3
        diff=0.07
        start_point_x=float(2)
        start_point_y=float(2)
        rospy.init_node("spiral_node",anonymous=True)

        spiral_pub=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
        rospy.Subscriber("/turtle1/pose", Pose, cb)
        start_point_PID(start_point_x,start_point_y,1)
        turn(start_point_x,start_point_y+6)
        i=0
        a=start_point_x
        b=start_point_y
        while True:
#            print('1',i,a,b)
            i+=1
#            print('2',i,a,b)
            if (i+3)%4==0:
                start_point_PID(a+(diff*(i/4)),b+6-(diff*(i/4)),0)
                turn(a+6-(diff*(i/4)),b+6-(diff*(i/4)))
            if (i+2)%4==0:
                start_point_PID(a+6-(diff*(i/4)),b+6-(diff*(i/4)),0)
                turn(a+6-(diff*(i/4)),b+(diff*(i/4)))
            if (i+1)%4==0:
                start_point_PID(a+6-(diff*(i/4)),b+(diff*(i+1/4)),0)
                turn(a+(diff*(i/4)),b+(diff*(i+1/4)))
 #               a+=(tolerance*(i/4))
 #               b+=(tolerance*(i/4))            
            if i%4==0:
                print('i4',i)
                print(a+(diff*(i/4)),b+(diff*(i/4)))
                start_point_PID(a+(diff*(i/4)),b+(diff*(i/4)),4)

                turn(a+(diff*(i/4)),b+6-(diff*(i/4)))

#            a+=(tolerance*(i/4))
#            b+=(tolerance*(i/4))
            print(msg_p)
#            print('3',i,a,b)
    except rospy.ROSInterruptException:
        pass