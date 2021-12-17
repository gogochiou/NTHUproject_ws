#!/usr/bin/env python
import rospy
import math
import numpy as np
# import pandas as pd
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import PointStamped

class pose():
    def __init__(self,x,y):
        self.timestamp = 0
        self.x = x
        self.y = y
        self.theta = 0
    
    def distance(self, p):
        return math.sqrt(pow(self.x-p.x, 2) + pow(self.y-p.y, 2))

class vector():
    def __init__(self, start, end):
        self.p1 = start
        self.p2 = end
        self.mat = np.matrix([[end.x - start.x], [end.y - start.y]])
        self.ang = 0
        self.len = 0
        self.mid_point = pose
    
    def matrix(self):
        return self.mat

    def mid_point(self):
        self.mid_point.x = (self.p1.x + self.p2.x)/2
        self.mid_point.y = (self.p1.y + self.p2.y)/2
        return self.mid_point
    
    def angle(self):
        self.ang = math.atan2(self.mat[1,0], self.mat[0,0])
        return self.ang
    
    def length(self):
        self.len = math.sqrt(self.mat[0,0]*self.mat[0,0] + self.mat[1,0]*self.mat[1,0])
        return self.len

    def rotate(self, theta):
        rot = np.matrix([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        self.mat = rot * self.mat  

    def scale(self, scale):
        self.mat[0, 0] *= scale
        self.mat[1, 0] *= scale

class linkage():
    def __init__(self, origin, length, angle):
        self.origin = origin
        self.length = length
        self.angle = angle
        self.joint_end = pose(0,0)

    def end_joint(self):
        self.joint_end.x = self.origin.x + self.length * math.cos(self.angle)
        self.joint_end.y = self.origin.y + self.length * math.sin(self.angle)
        return self.joint_end

class motor():
    def __init__(self, idx, ori, init_angle, span):
        self.origin = ori
        self.idx = idx
        self.angle = init_angle
        self.span = span    

    def stepper_angle(self):
        return self.angle

class scara():
    def __init__(self):
        self.target_sub = rospy.Subscriber("target", PointStamped, self.targetCallback)
        self.stepper_pub = rospy.Publisher("stepper_command", Float64MultiArray, queue_size=100)
        # self.stepper_sub = rospy.Subscriber("stepper_feedback", Float64MultiArray, self.stepperCallback)
        self.txst1_pub = rospy.Publisher("txARM", Int32MultiArray, queue_size=100)
        self.rxst1_sub = rospy.Subscriber("rxST1", Int32MultiArray, self.rxST1Callback)
        # linkages
        self.motor_L = motor(0, pose(-21-3.7/2, 0), math.radians(-170), [math.radians(190.01), math.radians(90)])
        self.motor_R = motor(1, pose(21+3.7/2, 0), math.radians(-10), [math.radians(-10.01), math.radians(90)])
        # print ("x,y"), self.motor_L.origin.x, self.motor_L.origin.y
        self.link_L1 = linkage(self.motor_L.origin, 141, math.radians(-170))
        self.link_R1 = linkage(self.motor_R.origin, 141, math.radians(-10))

        self.link_L2 = linkage(pose(0,0), 184, math.radians(-170))
        self.link_R2 = linkage(pose(0,0), 184, math.radians(-10))
        
        self.joint_L = pose(0,0)
        self.joint_R = pose(0,0)
        self.joint_end = pose(0,0)
        self.target_pose = pose(0, 100)
        self.stepper_feedback_received = 0
        # controller parameter (unit = mm)
        self.control_frequency = 5 #hz
        self.target_received = 0
        self.target_reached = 0
        self.stop_tolerance = 1
        self.K_pl = 1
        self.K_pr = 1
        self.K_p = 0.5
        self.speed_cur = 0
        self.speed_min = 0
        self.speed_max = 70
        self.acc_time = 1
        self.brake_dis = 40
        self.acc1 = (self.speed_max - self.speed_min)/(self.acc_time * self.control_frequency)
        self.acc2 = (self.speed_max**2 - self.speed_min**2)/(2*self.brake_dis)

    def rxST1Callback(self,data):
        self.motor_L.angle = self.theta_convert(float(data.data[3])/1000)
        self.motor_R.angle = self.theta_convert(float(data.data[4])/1000)
        # self.motor_R.angle = self.theta_convert(data.data[4]/1000)
        # print ("LR angle"), self.motor_L.angle, self.motor_R.angle
        self.joint_end = self.get_endjoint_pose()
        # print ("joint_end"), self.joint_end.x, self.joint_end.y
        self.stepper_feedback_received = 1

    # def stepperCallback(self, data):
    #     self.motor_L.angle = self.theta_convert(data.data[0])
    #     self.motor_R.angle = self.theta_convert(data.data[1])
    #     self.joint_end = self.get_endjoint_pose()
    #     # print ("joint_end"), self.joint_end.x, self.joint_end.y
    #     self.stepper_feedback_received = 1

    def targetCallback(self,data):
        # self.target_pose.timestamp = data.header.stamp
        if self.target_received == 0:
            self.target_pose.x = data.point.x
            self.target_pose.y = data.point.y
            print ("target received !"), (self.target_pose.x, self.target_pose.y)
            self.target_received = 1

        if self.target_reached == 1:
            # print ("target received !")
            self.target_reached = 0
            self.controller(self.target_pose)

    def init(self):
        print("Arm point tracking initialized")
        while not rospy.is_shutdown():
            # print("waiting for target !") 
            if self.target_received:
                self.controller(self.target_pose)

    # def controller(self,target):
    #     # print ("aaaaaaaaa")
    #     if self.stepper_feedback_received and self.joint_end.y != 0:
    #         print("controller started !")
    #     rate = rospy.Rate(self.control_frequency)
    #     while(self.joint_end.distance(target) > self.stop_tolerance):
    #         if rospy.is_shutdown():
    #             break
    #         if self.stepper_feedback_received:
    #             err = self.joint_end.distance(target)
    #             if (self.speed_cur < self.speed_max):
    #                 self.speed_cur += self.acc1
                
    #             if err < self.brake_dis:
    #                 self.speed_cur += self.acc1
    #                 limit = math.sqrt(err * self.acc2 )
    #                 if self.speed_cur >= limit:
    #                     self.speed_cur = limit
            
    #             # print ("joint end"), self.joint_end.x, self.joint_end.y
    #             v_x = self.speed_cur * math.cos(math.atan2(target.y - self.joint_end.y, target.x - self.joint_end.x))
    #             v_y = self.speed_cur * math.sin(math.atan2(target.y - self.joint_end.y, target.x - self.joint_end.x))
    #             # print("v_xy"), v_x, v_y
    #             self.arm_move(v_x, v_y)
            
    #         # if self.stepper_feedback_received:
    #         #     v_x = self.K_p * (target.x - self.joint_end.x)
    #         #     v_y = self.K_p * (target.y - self.joint_end.y)
    #         #     self.arm_move(v_x, v_y)

    #     self.target_reached = 1
    #     self.target_received = 0
    #     print ("target acheived !")

    def controller(self,target):
        # print ("aaaaaaaaa")
        pi = math.pi
        # if self.stepper_feedback_received and self.joint_end.y != 0:
        #     print("controller started !")
        rate = rospy.Rate(self.control_frequency)
        angle_L = self.get_stepper_angle(self.motor_L, target, self.link_L1, self.link_L2)
        angle_R = self.get_stepper_angle(self.motor_R, target, self.link_R1, self.link_R2)
        # angle_L = pi/2
        # angle_R = pi/2
        print ("target angle in deg"),  (math.degrees(angle_L), math.degrees(angle_R))
        reached_L = 0
        reached_R = 0
        vel_L = pi/3
        vel_R = pi/3
        while not rospy.is_shutdown():
            if reached_L == 1 and reached_R == 1:
                break

            if angle_L * self.motor_L.angle < 0:
                if angle_L - self.motor_L.angle > 0:
                    vel_L = -pi/3
            else:
                if angle_L - self.motor_L.angle < 0:
                    vel_L = -pi/3
                    
            if angle_R - self.motor_R.angle < 0:
                vel_R = -pi/3

            if abs(angle_L - self.motor_L.angle) < 0.1:
                # print("aaaaaa")
                vel_L = 0
                reached_L = 1
            if abs(angle_R - self.motor_R.angle) < 0.1:
                # print("bbbbbb")
                vel_R = 0
                reached_R = 1
            print ("current vel"), (vel_L, vel_R)
            self.stepper_speed_publish(vel_L, vel_R)
        self.stepper_speed_publish(0, 0)
        self.target_reached = 1
        self.target_received = 0
        print ("target acheived !")

    def arm_move(self, v_x, v_y):
        d_t = 1/float(self.control_frequency)
        # print d_t
        next_point = pose(self.joint_end.x + v_x*d_t, self.joint_end.y + v_y*d_t)
        # print ("current target")
        
        # print ("nextpoint"), next_point.x, next_point.y
        print ("stepper angle"),(self.get_stepper_angle(self.motor_L, next_point, self.link_L1, self.link_L2), self.get_stepper_angle(self.motor_R, next_point, self.link_L1, self.link_L2))
        self.stepper_moveto(self.get_stepper_angle(self.motor_L, next_point, self.link_L1, self.link_L2), self.get_stepper_angle(self.motor_R, next_point, self.link_L1, self.link_L2))

    def get_endjoint_pose(self):
        # update linkages
        self.link_L1.angle = self.motor_L.stepper_angle()
        self.link_R1.angle = self.motor_R.stepper_angle()
        
        self.link_L2.origin = self.link_L1.end_joint()
        self.link_R2.origin = self.link_R1.end_joint()
        
        joint_vec = vector(self.link_L2.origin, self.link_R2.origin)
        t1 = joint_vec.length()/2
        t2 = math.sqrt(pow(self.link_L2.length,2) - pow(t1, 2))

        self.link_L2.angle = joint_vec.angle() + math.atan2(t2, t1)
        # self.link_R2.angle = joint_vec.angle() + math.radians(180) - math.atan2(t2, t1)
        return self.link_L2.end_joint()

    def get_stepper_angle(self, motor, target, link1, link2):
        #inverse kinematics
        mt_vec = vector(motor.origin, target)
        l3 = mt_vec.length()
        l1 = link1.length
        l2 =  link2.length
        # print motor.idx
        # print target.x, target.y
        # print l1, l2, l3
        # print (pow(l1, 2)+pow(l3, 2)-pow(l2, 2))/2/l1/l3
        theta_l2 = math.acos((pow(l1, 2)+pow(l3, 2)-pow(l2, 2))/2/l1/l3)
        if motor.idx == 0:
            angle = mt_vec.angle() + theta_l2
        else:
            angle = mt_vec.angle() - theta_l2
        return angle
    
    def stepper_moveto(self, angle_L, angle_R):
        # if self.motor_L.angle == self.motor_L.span[0] or self.motor_L.angle == self.motor_L.span[1]:
        #     self.K_pl *= -1
        # if self.motor_R.angle == self.motor_R.span[0] or self.motor_R.angle == self.motor_R.span[1]:
        #     self.K_pr *= -1
        # vel_L = self.K_pl * self.theta_convert((angle_L - self.motor_L.angle))
        # vel_R = self.K_pr * self.theta_convert((angle_R - self.motor_R.angle))
        d_t = 1/float(self.control_frequency)
        if angle_L > self.motor_L.angle:
            vel_L = -1 * (angle_L - self.motor_L.angle)/d_t
        else:
            vel_L = (angle_L - self.motor_L.angle)/d_t

        if angle_L > self.motor_L.angle:
            vel_R = -1 * (angle_R - self.motor_R.angle)/d_t
        else:
            vel_R = (angle_R - self.motor_R.angle)/d_t
        
        vel = Float64MultiArray()
        vel.data = [self.theta_convert(vel_L), self.theta_convert(vel_R)]
        print vel.data
        # self.stepper_pub.publish(vel)  
        self.stepper_speed_publish(vel_L, vel_R)

    def stepper_speed_publish(self, vl, vr):
        vel = Float64MultiArray()
        vel.data = [vl, vr]
        # print("current stepper output"), vel.data
        self.stepper_pub.publish(vel)
        vel_int = Int32MultiArray()
        vel_int.data = [int(vl*1000), int(vr*1000)]
        # vel_int.data = [0,0,0,int(vl*1000), int(vr*1000),0,0] 
        self.txst1_pub.publish(vel_int) 

    def theta_convert(self, input):
        pi = math.pi
        # convert rad domain to [-pi, pi]
        if input >=0:
            input = math.fmod(input, 2*pi)
            if input > pi:
                input -= 2*pi
                output = input
            else:
                output = input
        else:
            input *= -1
            input = math.fmod(input, 2*pi)
            if input > pi:
                input -= 2*pi
                output = input*-1
            else:
                output = input*-1
        return output

if __name__ == '__main__':
    try:
        rospy.init_node('arm_controller', anonymous = True)
        arm = scara()
        arm.init()

    except rospy.ROSInterruptException:
        pass