#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
class HallwayNav():
    def __init__(self):
        rospy.init_node('HallwayNavigator')
        self.range_sub = rospy.Subscriber('simple_skid_steer/laser/scan', LaserScan, self.range_callback)
        self.twist_pub = rospy.Publisher('simple_skid_steer/cmd_vel', Twist, queue_size = 10)
        self.vel = Twist()
        self.simplified_scan = [0, 0, 0, 0, 0]
        self.navigate()

    def range_callback(self, msg):
        self.simplified_scan[0] = msg.ranges[int(len(msg.ranges) / 2)]
        self.simplified_scan[1] = max(msg.ranges)
        self.simplified_scan[2] = min(msg.ranges)
        self.simplified_scan[3] = msg.ranges[0]
        self.simplified_scan[4] = msg.ranges[len(msg.ranges) - 1]

    def navigate(self):
        while not (rospy.is_shutdown()):
            if(self.simplified_scan[0] < .65 or self.simplified_scan[2] < .35):
                self.vel.linear.x = 0
                if(self.simplified_scan[4] < self.simplified_scan[3]):
                    self.vel.angular.z = 3
                else:
                    self.vel.angular.z = -3
                if(self.simplified_scan[4] + .1 > self.simplified_scan[3] and self.simplified_scan[4] - .1 < self.simplified_scan[3]):
                    self.vel.angular.z = 3
            else:
                self.vel.angular.z = 0
                self.vel.linear.x = 1
            self.twist_pub.publish(self.vel)
            
if __name__=='___main__':
    my_nav = HallwayNav()
