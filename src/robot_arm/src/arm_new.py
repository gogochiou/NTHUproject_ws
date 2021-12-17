#!/usr/bin/env python
import rospy
import math
import numpy as np
import tools
# import pandas as pd
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import PointStamped
from robot_arm.msg import armCommand
from robot_arm.msg import armState

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
        self.target_sub = rospy.Subscriber("point_output", PointStamped, self.targetCallback)
        self.stepper_pub = rospy.Publisher("stepper_command", Float64MultiArray, queue_size=100)
        # self.stepper_sub = rospy.Subscriber("stepper_feedback", Float64MultiArray, self.stepperCallback)
        self.txst1_pub = rospy.Publisher("txARM", Int32MultiArray, queue_size=100)
        self.rxst1_sub = rospy.Subscriber("rxST1", Int32MultiArray, self.rxST1Callback)
        self.main_to_arm = rospy.Subscriber("arm_mission", armCommand, self.mainCallback)
        self.arm_to_main = rospy.Publisher("arm_to_main", armState, queue_size=100)
        # linkages
        self.motor_L = motor(0, pose(-21-3.7/2, 0), math.radians(-170), [math.radians(190.01), math.radians(90)])
        self.motor_R = motor(1, pose(21+3.7/2, 0), math.radians(-10), [math.radians(-10.01), math.radians(90)])
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
        self.target_executing = 0
        self.stop_tolerance = 0.1
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
        # sucker
        # Grab 0, Release 1, Hold 2
        self.home_pose = pose(49.315, 121.264)
        self.release_pose = pose(0, 200)
        self.task_received = 0
        self.sucker_task = "Hold"
        self.sucker_color = "No"
        self.sucker_feedback = "Success"
        # success 1, fail 0, executing 2

    def rxST1Callback(self,data):
        self.motor_L.angle = tools.theta_convert(float(data.data[3])/1000)
        self.motor_R.angle = tools.theta_convert(float(data.data[4])/1000)
        # print("stepper angle feedback"), self.motor_L.angle, self.motor_R.angle
        if data.data[5] == 0:
            self.sucker_feedback = "Fail"
        if data.data[5] == 1:
            self.sucker_feedback = "Success"
        if data.data[5] == 2:
            self.sucker_feedback = "Executing"
        # self.motor_R.angle = tools.theta_convert(data.data[4]/1000)
        # print ("LR angle"), self.motor_L.angle, self.motor_R.angle
        self.joint_end = self.get_endjoint_pose()
        # print ("joint_end"), self.joint_end.x, self.joint_end.y
        self.stepper_feedback_received = 1

    def targetCallback(self,data):
        if self.target_received == 0 and self.target_executing == 0:
            self.target_pose = self.base2arm(pose(data.point.x, data.point.y))
            print("cam"), (data.point.x, data.point.y)
            print ("target received !"), (self.target_pose.x, self.target_pose.y) 
            self.target_received = 1

    def mainCallback(self, data):
        # Release Grab Hold
        self.sucker_task = data.action
        print("main request"), data.action
        self.task_received = 1

    def base2arm(self,input):
        x = -1*input.y * 1000
        y = input.x * 1000 - 49.9
        return pose(x, y)

    def init(self):
        print("Arm point tracking initialized")
        print("waiting for target !") 
        while not rospy.is_shutdown():
            if self.target_received and self.sucker_task == "Grab":
                self.controller(self.target_pose)
                if self.task_received:
                    while not self.sucker_feedback == "Executing" and not rospy.is_shutdown():
                        self.sucker_publish(self.sucker_task)
                        # print("sucker executing ...")
                        pass
                    while (not self.sucker_feedback == "Success" and not self.sucker_feedback == "Fail") and not rospy.is_shutdown():
                        pass                    
                    self.sucker_publish("Hold")
                    self.controller(self.home_pose)
                self.stepper_speed_publish(0, 0)
                self.target_received = 0
                self.task_received = 0
                self.sucker_task = "Hold"       

            if self.sucker_task == "Release":
                self.controller(self.release_pose)
                if self.task_received:
                    while not self.sucker_feedback == "Executing" and not rospy.is_shutdown():
                        self.sucker_publish(self.sucker_task)
                        print("sucker executing ...")
                        pass
                    while (not self.sucker_feedback == "Success" and not self.sucker_feedback == "Fail") and not rospy.is_shutdown():
                        pass                    
                    self.sucker_publish("Hold")
                    self.controller(self.home_pose)
                self.stepper_speed_publish(0, 0)
                self.target_received = 0
                self.sucker_task = "Hold" 
            
        #    rate = rospy.Rate(50)
        #    while not rospy.is_shutdown():
        #      	print self.motor_R.angle
        #      	if abs(self.motor_R.angle - 1.57) > 0.1 :
        #        	self.stepper_speed_publish(0,1)
        #    	else:
        #        	self.stepper_speed_publish(0,0)
        #        	break
	#	rate.sleep()

    def stepper_safe(self, motor, dir):
        if abs(motor.angle - motor.span[0]) < self.stop_tolerance:
            if motor.idx == 0:
                if dir == 1:
                    return 0
                else:
                    return 1
            if motor.idx == 1:
                if dir == 1 or dir == 0:
                    return 1
                else:
                    return 0
                    
        elif abs(motor.angle - motor.span[1]) < self.stop_tolerance:
            if motor.idx == 0:
                if dir == 1 or dir == 0:
                    return 1
                else:
                    return 0
            if motor.idx == 1:
                if dir == 1:
                    return 0
                else:
                    return 1
        else:
            return 1
                
    def controller(self,target):
        self.target_executing = 1
        pi = math.pi
        if self.get_stepper_angle(self.motor_L, target, self.link_L1, self.link_L2) == "domain error" or self.get_stepper_angle(self.motor_R, target, self.link_R1, self.link_R2) == "error":
            print("Target out of range !!!!")
            self.stepper_speed_publish(0, 0)
        else:
            angle_L = self.get_stepper_angle(self.motor_L, target, self.link_L1, self.link_L2)
            angle_R = self.get_stepper_angle(self.motor_R, target, self.link_R1, self.link_R2)
            print ("target angle in deg"),  (math.degrees(angle_L), math.degrees(angle_R))
            reached_L = 0
            reached_R = 0
            vel = 0.5 *pi/3
            vel_L = vel
            vel_R = vel
            rate = rospy.Rate(self.control_frequency)
            while not rospy.is_shutdown():
                if reached_L == 1 and reached_R == 1:
                    break
                if angle_L * self.motor_L.angle < 0:
                    if angle_L - self.motor_L.angle > 0:
                        vel_L = -vel
                else:
                    if angle_L - self.motor_L.angle < 0:
                        vel_L = -vel
            
                if angle_R - self.motor_R.angle < 0:
                    vel_R = -vel

                if abs(angle_L - self.motor_L.angle) < 0.1:
                    vel_L = 0
                    reached_L = 1
                if abs(angle_R - self.motor_R.angle) < 0.1:
                    vel_R = 0
                    reached_R = 1
                # print("current angle"), (math.degrees(self.motor_L.angle), math.degrees(self.motor_R.angle))
                # print ("current vel"), (vel_L, vel_R)
                if not self.stepper_safe(self.motor_L, np.sign(vel_L)):
                    vel_L = 0
                    print("left stepper danger !!!!!")
                if not self.stepper_safe(self.motor_R, np.sign(vel_R)):
                    vel_R = 0
                    print("right stepper danger !!!!!")
                self.stepper_speed_publish(vel_L, vel_R)
		#		rate.sleep()

            self.stepper_speed_publish(0, 0)
            self.target_executing = 0
            print ("target acheived !")

    def sucker_transmit(self, task):
        if task == "Grab":
            return 0
        if task == "Release":
            return 1
        if task == "Hold":
            return 2

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
        k = (pow(l1, 2)+pow(l3, 2)-pow(l2, 2))/2/l1/l3
        if k <=1 and k >= -1:
            theta_l2 = math.acos((pow(l1, 2)+pow(l3, 2)-pow(l2, 2))/2/l1/l3)
            if motor.idx == 0:
                angle = mt_vec.angle() + theta_l2
            else:
                angle = mt_vec.angle() - theta_l2
            return angle
        else:
            return "domain error"
    
    def stepper_moveto(self, angle_L, angle_R):
        d_t = 1/float(self.control_frequency)
        if angle_L > self.motor_L.angle:
            vel_L = -1 * (angle_L - self.motor_L.angle)/d_t
        else:
            vel_L = (angle_L - self.motor_L.angle)/d_t

        if angle_L > self.motor_L.angle:
            vel_R = -1 * (angle_R - self.motor_R.angle)/d_t
        else:
            vel_R = (angle_R - self.motor_R.angle)/d_t
        
        self.stepper_speed_publish(vel_L, vel_R)

    def stepper_speed_publish(self, vl, vr):
        vel = Float64MultiArray()
        vel.data = [vl, vr]
        # print("current stepper output"), vel.data
        # self.stepper_pub.publish(vel)
        vel_int = Int32MultiArray()
        vel_int.data = [int(vl*1000), int(vr*1000), self.sucker_transmit("Hold")]
        # vel_int.data = [0,0,0,int(vl*1000), int(vr*1000),0,0] 
        self.txst1_pub.publish(vel_int) 

    def sucker_publish(self, task):
        arr = Int32MultiArray()
        arr.data = [0,0, self.sucker_transmit(task)]
        self.txst1_pub.publish(arr) 

if __name__ == '__main__':
    try:
        rospy.init_node('arm_controller', anonymous = True)
        arm = scara()
        arm.init()

    except rospy.ROSInterruptException:
        pass
