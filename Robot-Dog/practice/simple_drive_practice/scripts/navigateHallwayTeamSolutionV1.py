#!/usr/bin/env python3
#This script was authored collectively by the ROS and Gazebo team on 10/03/2021 at the software sync in Richards 440
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class HallwayNav():
    def __init__(self):
        '''
        A class to represent avoiding obstacles which generally progressing forwards
        for a robot that produces laserscan sensor data and whos movement is controlled by the twist msg

        This publishes to the following topics:
            simple_skid_steer/laser/scan (line 35)

        This subscribes to the following topics:
            simple_skid_steer/cmd_vel (line 36)

        Attributes:
        --------------
        range_sub: The ROS subscriber to take in scan (sensor_msgs.msg/LaserScan) data
        twist_pub: The ROS publisher that publishes twist (geometry_msgs.msg/Twist) commands to robot 

        scan: what the robot sees, copied from the ROS topic into the program
        select_scan_data: certain pertinent infomration that is obtained from scan

        Methods:
        --------------
        navigate: uses conditional statements to avoid obstacles based off of laserscan data
        find_max_index: determines which scan index has the largest value; effectively what direction has things the furthest away
        
        '''

        rospy.init_node('HallwayNavigator')
        self.range_sub = rospy.Subscriber('simple_skid_steer/laser/scan', LaserScan, self.scan_callback) 
        self.twist_pub = rospy.Publisher('simple_skid_steer/cmd_vel', Twist, queue_size = 10)
        self.vel = Twist() #modify and publish this message to move the robot
        self.scan = [] 
        self.select_scan_data = [0, #index 0 corresponds to minimum distance
                                 0, #index 1 corresponds to maximum distance
                                 0] #index 2 corresponds to distance directly ahead of the robot
        self.navigate()
        
    def scan_callback(self, scan_msg):
        self.scan = scan_msg.ranges #all sensor data ranges in an array
        self.select_scan_data[0] = scan_msg.range_min #maximum read range from sensor data
        self.select_scan_data[1]= scan_msg.range_max  #minimum read range from sensor data
        self.select_scan_data[2] = scan_msg.ranges[int(len(scan_msg.ranges) / 2)] #what is directly ahead of the robot 

    def navigate(self):
        TOLERANCE = .1 #how close the distance directly ahead of the robot has to be to the maximum possible distance for the robot to proceed forwards
        while not (rospy.is_shutdown()):
            turn_direction = 0
            #if what is directly ahead of the robot is NOT almost the path of least resistance:
            if (abs(self.select_scan_data[2] - self.select_scan_data[1]) > TOLERANCE): 
                #determines direction of turn: compares the index of the maximum value with index of what is ahead 
                if (self.find_max_index(self.scan, self.select_scan_data[1]) > int(len(self.scan) / 2)):
                    turn_direction = -1
                else:
                    turn_direction = 1
                
                #turn in the proper direction while staying still
                self.vel.angular.z = turn_direction * 2
                self.vel.linear.x = 0 

            else:
                #move forwards without turning
                self.vel.linear.x = 1
                self.vel.angular.z = turn_direction
            
            self.twist_pub.publish(self.vel) #sets the robot velocity to the desired velocity

    #find_max_index: HallwayNav Array Float32 -> Int
    def find_max_index(self, scan, max_val):
        # scan is an array that contains all distances as part of laser scan's ranges
        # max_val is the maximum possible distance read by the laser scan
        # iterates through each index of scan, and compares the value @the index to the maximum value contained in the scan message
        for x in range(len(scan)):
            if scan[x] == max_val:
                return x
            
if __name__ == '__main__':
    my_nav = HallwayNav()
