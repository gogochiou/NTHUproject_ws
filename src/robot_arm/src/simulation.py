#!/usr/bin/env python
import rospy
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Float64MultiArray

class pose():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, p):
        return math.sqrt(pow(self.x-p.x, 2) + pow(self.y-p.y, 2))

class vector():
    def __init__(self, start, end):
        self.p1 = start
        self.p2 = end
        self.mat = np.matrix([[end.x - start.x], [end.y - start.y]])
        self.ang = 0
        self.len = 0
        self.mid_point = pose(0,0)    
    
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
    def __init__(self, idx, origin, init_angle, span):
        # self.stepper_sub = rospy.Subscriber("stepper_command", Float64MultiArray, self.stepperCallback)
        self.origin = origin
        self.idx = idx
        self.angle = init_angle
        self.span = span
        self.speed = 0
        self.time_p = 0
        self.delta_t = 0        
    
    def stepperCallback(self, data):
        self.speed = data.data[self.idx]
        if self.time_p ==0:
            self.time_p = rospy.get_time()
        else:
            self.delta_t = rospy.get_time() - self.time_p
        self.time_p = rospy.get_time()
        
        self.angle += self.delta_t * self.speed

    def stepper_angle(self):
        return self.angle

    def move(self, rad):
        self.angle = rad
        
class scara():
    def __init__(self):
        self.stepper_pub = rospy.Publisher("stepper_feedback", Float64MultiArray, queue_size=100)
        self.target_pub = rospy.Publisher("target", PointStamped, queue_size=100)
        self.stepper_sub = rospy.Subscriber("stepper_command", Float64MultiArray, self.stepperCallback)
        self.stepper_command = Float64MultiArray()
        # mechanical parameter
        self.motor_L = motor(0, pose(-21, 0), math.radians(-170), [math.radians(190.01), math.radians(90)])
        self.motor_R = motor(1, pose(21, 0), math.radians(-10), [math.radians(-10.01), math.radians(90)])

        self.link_L1 = linkage(self.motor_L.origin, 141, math.radians(-170))
        self.link_R1 = linkage(self.motor_R.origin, 141, math.radians(-10))

        self.link_L2 = linkage(pose(0,0), 184, math.radians(-170))
        self.link_R2 = linkage(pose(0,0), 184, math.radians(-10))
        
        self.joint_L = pose(0,0)
        self.joint_R = pose(0,0)
        self.joint_end = pose(0,0)
        self.joint_end_x = []
        self.joint_end_y = []
        
        # span iteration
        self.iteration = 0
        self.iter_size = 80
        self.l_linspace = np.linspace(self.motor_L.span[0], self.motor_L.span[1], num = self.iter_size)
        self.r_linspace = np.linspace(self.motor_R.span[0], self.motor_R.span[1], num = self.iter_size)
        self.count = 0
        self.l = 0
        self.r = 0

        # VISUALIZATION
        self.show_locus = 1
        self.save = 0
        self.filename = '/home/guanlunlu/catkin_ws/src/robot_arm/src/arm_span_80_int.csv'    
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-350, 350), ylim=(-150, 350))
        self.line1, = self.ax.plot([], [], lw=8)
        self.line2, = self.ax.plot([], [], lw=8)
        self.line3, = self.ax.plot([], [], lw=8)
        self.line4, = self.ax.plot([], [], lw=8)        
        self.locus, = self.ax.plot([], [], lw=2, c = "g")

        # target
        self.targetList = [pose(0,300), pose(50,150), pose(-50,150), pose(0,300), pose(-100,200), pose(0, 200), pose(100, 200), pose(0,300)]
        self.current_target = pose(0,0)
        self.target_approach = 0
        
    def stepperCallback(self, data):
        self.stepper_command = data 
        self.motor_L.stepperCallback(self.stepper_command)
        self.motor_R.stepperCallback(self.stepper_command)
        
    def target_update(self):
        if self.joint_end.distance(self.current_target) < 2:
            print ("target acheived !")
            self.target_approach = 1
            self.time_p = 0
            if self.targetList:
                self.current_target = self.targetList.pop()
                plt.scatter(self.current_target.x, self.current_target.y,c="red", alpha= 1,s = 20, marker = "D")
            else:
                print ("target all acheived !")
        msg = PointStamped()
        # msg.header.stamp = rospy.get_time()
        msg.point.x = self.current_target.x
        msg.point.y = self.current_target.y
        self.target_pub.publish(msg)

    def initialize(self):
        if self.targetList:
            self.current_target = self.targetList.pop()
        print ("simulation start !")
        print ("current target :"), (self.current_target.x, self.current_target.y)
        self.visualize()
        self.save_locus()

    def iteration_span(self):
        if self.iteration ==1:
            if self.count < pow(self.iter_size, 2):
                if(self.count %self.iter_size ==0):
                    if self.count/self.iter_size < self.iter_size:
                        self.l = self.l_linspace[self.count/self.iter_size]
                self.r = self.r_linspace[self.count %self.iter_size]
                self.count +=1
                self.motor_L.move(self.l)
                self.motor_R.move(self.r)

    def simulation_update(self):
        self.iteration_span()
        # self.target_update()
        # update linkages
        self.link_L1.angle = self.motor_L.stepper_angle()
        self.link_R1.angle = self.motor_R.stepper_angle()
        
        self.link_L2.origin = self.link_L1.end_joint()
        self.link_R2.origin = self.link_R1.end_joint()
        
        joint_vec = vector(self.link_L2.origin, self.link_R2.origin)
        t1 = joint_vec.length()/2
        t2 = math.sqrt(pow(self.link_L2.length,2) - pow(t1, 2))

        self.link_L2.angle = joint_vec.angle() + math.atan2(t2, t1)
        self.link_R2.angle = joint_vec.angle() + math.radians(180) - math.atan2(t2, t1)
        self.joint_end = self.link_L2.end_joint()
        # show_locus
        if self.show_locus == 1:
            self.joint_end_x.append(int(self.link_L2.end_joint().x))
            self.joint_end_y.append(int(self.link_L2.end_joint().y))
        
        self.stepper_feedback()
        # print ("current target"), self.current_target.x, self.current_target.y

    def stepper_feedback(self):
        msg = Float64MultiArray()
        msg.data = [self.motor_L.angle, self.motor_R.angle]
        # print msg.data
        self.stepper_pub.publish(msg)
        self.target_update()                

    def save_locus(self):
        if self.save == 1:
            dict = {'x' : self.joint_end_x, 'y' : self.joint_end_y}
            df = pd.DataFrame(dict)
            df.to_csv(self.filename) 
            print ("data saved !")

    def animation_init(self):
        self.line1.set_data([], [])
        self.line2.set_data([], [])
        self.line3.set_data([], [])
        self.line4.set_data([], [])
        self.locus.set_data([], [])
        return self.line1, self.line2, self.line3, self.line4, self.locus,

    def animate(self, i):
        self.simulation_update()
        # linkage 1
        r1 = np.linspace(0,self.link_L1.length, self.iter_size)
        L1_x = self.motor_L.origin.x + r1*math.cos(self.link_L1.angle)
        L1_y = r1*math.sin(self.link_L1.angle)
        self.line1.set_data(L1_x,L1_y)
        
        R1_x = self.motor_R.origin.x + r1*math.cos(self.link_R1.angle)
        R1_y = r1*math.sin(self.link_R1.angle)
        self.line2.set_data(R1_x,R1_y)

        #linkage 2
        r2 = np.linspace(0,self.link_L2.length, self.iter_size)
        L2_x = self.link_L2.origin.x + r2*math.cos(self.link_L2.angle)
        L2_y = self.link_L2.origin.y + r2*math.sin(self.link_L2.angle)
        self.line3.set_data(L2_x,L2_y)
        
        R2_x = self.link_R2.origin.x + r2*math.cos(self.link_R2.angle)
        R2_y = self.link_R2.origin.y + r2*math.sin(self.link_R2.angle)
        self.line4.set_data(R2_x,R2_y)
        # print self.joint_end_x
        #locus
        self.locus.set_data(self.joint_end_x, self.joint_end_y)

        a = plt.scatter(self.current_target.x, self.current_target.y,c="red", alpha= 1,s = 20, marker = "D")
        #show target
        return self.line1, self.line2, self.line3, self.line4, self.locus, a,

    def show_span(self):
        data = open('/home/guanlunlu/catkin_ws/src/robot_arm/src/arm_span_80.csv', 'r')
        # data = open('~/catkin_ws/src/robot_arm/src/arm_span_80.csv', 'r')
        span = pd.read_csv(data)
        span = span.values.tolist()
        x = []
        y = []
        for i in span:
            x.append(i[1])
            y.append(i[2])
        plt.scatter(x,y,c="lightsteelblue", alpha= 0.3,s = 10, marker = "D")
        # plt.scatter(span["x"], span["y"], c = "m", s = 50, alpha = .5, marker = "D")

    def draw_hexagon(self):
        theta = np.linspace(0, 2*np.pi, 13)
        x = np.cos(theta)
        x[1::2] *= 144
        y = np.sin(theta)
        y[1::2] *= 144
        x[::2] *= 144
        y[::2] *= 144
        y[::2] += -50
        plt.plot(x[::2], y[::2], color='slategrey', alpha = 0.3)
        plt.fill(x[::2], y[::2], color='slategrey', alpha = 0.3)
        
    def visualize(self):
        draw_circle = plt.Circle((0, -50), 144,fill=False)
        self.show_span()
        self.draw_hexagon()
        # plt.gcf().gca().add_artist(draw_circle)
        anim = FuncAnimation(self.fig, self.animate, init_func=self.animation_init, frames=200, interval=10, blit=True)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid()
        plt.show()

if __name__ == '__main__':
    try:
        rospy.init_node('arm_simulation', anonymous = True)
        arm = scara()
        arm.initialize()
        # arm.visualize()
        # arm.save_locus()
        # arm.temp()
    except rospy.ROSInterruptException:
        pass