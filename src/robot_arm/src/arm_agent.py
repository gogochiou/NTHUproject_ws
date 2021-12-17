#!/usr/bin/env python
import rospy
import math
import numpy as np
import os

from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import PointStamped
from robot_arm import armState
from robot_arm import armCommand

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
        self.motor_L.angle = self.theta_convert(math.radians(data.data[4]/1000))
        self.motor_R.angle = self.theta_convert(math.radians(data.data[5]/1000))
        self.joint_end = self.get_endjoint_pose()
        # print ("joint_end"), self.joint_end.x, self.joint_end.y
        self.stepper_feedback_received = 1

    def targetCallback(self,data):
        # self.target_pose.timestamp = data.header.stamp
        self.target_pose.x = data.point.x
        self.target_pose.y = data.point.y
        # print ("target received !")
        if self.target_reached == 1:
            # print ("target received !")
            self.target_reached = 0
            self.controller(self.target_pose)

    def init(self):
        print("waiting for target !")
        self.controller(self.target_pose)

    def controller(self,target):
        if self.stepper_feedback_received and self.joint_end.y != 0:
            print("controller started !")
        rate = rospy.Rate(self.control_frequency)
        while(self.joint_end.distance(target) > self.stop_tolerance):
            if rospy.is_shutdown():
                break
            if self.stepper_feedback_received:
                err = self.joint_end.distance(target)
                if (self.speed_cur < self.speed_max):
                    self.speed_cur += self.acc1
                
                if err < self.brake_dis:
                    self.speed_cur += self.acc1
                    limit = math.sqrt(err * self.acc2 )
                    if self.speed_cur >= limit:
                        self.speed_cur = limit
                v_x = self.speed_cur * math.cos(math.atan2(target.y - self.joint_end.y, target.x - self.joint_end.x))
                v_y = self.speed_cur * math.sin(math.atan2(target.y - self.joint_end.y, target.x - self.joint_end.x))
                # print("v_xy"), v_x, v_y
                self.arm_move(v_x, v_y)
            
            # if self.stepper_feedback_received:
            #     v_x = self.K_p * (target.x - self.joint_end.x)
            #     v_y = self.K_p * (target.y - self.joint_end.y)
            #     self.arm_move(v_x, v_y)

        self.target_reached = 1
        print ("target acheived !")

    def arm_move(self, v_x, v_y):
        d_t = 1/float(self.control_frequency)
        # print d_t
        next_point = pose(self.joint_end.x + v_x*d_t, self.joint_end.y + v_y*d_t)
        # print ("current target")
        
        # print ("nextpoint"), next_point.x, next_point.y
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
        d_t = 1/float(self.control_frequency)
        vel_L = (angle_L - self.motor_L.angle)/d_t
        vel_R = (angle_R - self.motor_R.angle)/d_t
        vel = Float64MultiArray()
        vel.data = [self.theta_convert(vel_L), self.theta_convert(vel_R)]
        self.stepper_pub.publish(vel)  

    def stepper_speed_publish(self, vl, vr):
        vel = Float64MultiArray()
        vel.data = [vl, vr]
        print("current stepper output"), vel.data
        self.stepper_pub.publish(vel)

        vel_int = Int32MultiArray()
        vel_int.data = [0,0,0,int(vl*1000), int(vr*1000),0,0] 
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

class agent():
    def __init__(self):
        self.mission_sub = rospy.Subscriber("mission_request", armCommand, self.missionCallback)
        self.mission_pub = rospy.Publisher("mission_state", armState, queue_size=100)
        self.camera_pub = rospy.
        

        self.current_state = "Idle"
        self.action_req = "Hold"
        self.color_req = "Blue"
        self.missionFeedback = "Success"

    def missionCallback(self, data):
        self.action_req = data.action
        self.color_req = data.color
        self.current_state = "Operating"
    
    def init(self):
        print("Robot arm agent initialized !")
        print("Waiting for mission")
        while not rospy.is_shutdown() and self.current_state == "Operating":
            print ("current mission : "), (self.action_req, self.color_req)
            

    def activate_camera(self):
        os.system('')
    
    def deactivate_camera(self):
        os.system('')
        

if __name__ == '__main__':
    try:
        rospy.init_node('arm_agent', anonymous = True)
        arm = scara()
        arm.init()

    except rospy.ROSInterruptException:
        pass