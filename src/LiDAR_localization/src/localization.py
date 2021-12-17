#!/usr/bin/env python
import rospy
import math
import numpy as np
import itertools
import tf
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseWithCovarianceStamped
from obstacle_detector.msg import Obstacles
from obstacle_detector.msg import CircleObstacle
from std_msgs.msg import String
pi = math.pi

class pose():
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
    
    def distanceto(self, p):
        return math.sqrt(pow(self.x-p.x, 2) + pow(self.y-p.y, 2))

    def show(self):
        print (self.x, self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        pass

class vector():
    def __init__(self, start, end):
        self.p1 = start
        self.p2 = end
        self.d_x = end.x - start.x
        self.d_y = end.y - start.y
        self.mat = np.matrix([[end.x - start.x], [end.y - start.y]])
        self.ang = 0
        self.len = math.sqrt(self.mat[0,0]*self.mat[0,0] + self.mat[1,0]*self.mat[1,0])
        self.midpoint = pose(0,0,0)    
    
    def matrix(self):
        return self.mat

    def mid_point(self):
        self.midpoint.x = (self.p1.x + self.p2.x)/2
        self.midpoint.y = (self.p1.y + self.p2.y)/2
        return self.midpoint
    
    def angle(self):
        self.ang = math.atan2(self.mat[1,0], self.mat[0,0])
        return self.ang
    
    def length(self):
        self.len = math.sqrt(self.mat[0,0]*self.mat[0,0] + self.mat[1,0]*self.mat[1,0])
        return self.len

    def unit_vector(self):
        d_x = (self.p2.x - self.p1.x)/self.length()
        d_y = (self.p2.y - self.p1.y)/self.length()
        new_endpoint = pose(self.p1.x + d_x, self.p1.y + d_y, 0)
        return vector(self.p1, new_endpoint)

    def rotate(self, theta):
        rot = np.matrix([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        mat = rot * self.mat
        new_endpoint = pose(self.p1.x + mat[0,0], self.p1.y + mat[1,0], 0)
        return vector(self.p1, new_endpoint)

    def scale(self, scale):
        self.mat[0, 0] *= scale
        self.mat[1, 0] *= scale

class localization():
    def __init__(self):
        self.obstacleSub = rospy.Subscriber("/raw_obstacles", Obstacles, self.obstacleCallback)
        self.posePub = rospy.Publisher('lidar_bonbonbon', PoseWithCovarianceStamped, queue_size=10)
        self.tf_listener = tf.TransformListener()
        self.landmark_rviz = rospy.Publisher('landmark_extracted', Obstacles, queue_size=10)
        self.landmark1 = pose(-0.05, 1.0, 0)
        self.landmark2 = pose(2.05, 0.25, 0)
        self.landmark3 = pose(2.05, 1.75, 0)
        self.landmarkList = [self.landmark1, self.landmark2, self.landmark3]
        self.filter_threshold = 0.65
        self.landmark_extraction_threshold = 1 # 0.6
        self.sss_equiv_threshold = 0.07
        # self.field_mode = "wall"
        self.field_mode = "no wall"

    def obstacleCallback(self, data):
        obstacleList = []
        for i in data.circles:
            # rospy.loginfo("r", i.radius)
            # if i.radius > self.filter_threshold:
            obstacleList.append(pose(i.center.x, i.center.y, 0))
        if self.field_mode == "wall":
            self.trilateration(obstacleList, self.landmarkList)
            
        elif self.field_mode == "no wall":
            extractedList = self.landmark_extraction(obstacleList)
            if extractedList != "Not found":
                self.show_landmark_extracted(extractedList)
                self.trilateration(extractedList, self.landmarkList)
            else:
                print("Landmark Not Found !")

    def init(self):
        # while not rospy.is_shutdown():
        #     print("waiting for transform")
        #     if self.tf_listener.canTransform('landmark1', 'map', rospy.Time.now()) and self.tf_listener.canTransform('landmark2', 'map', rospy.Time.now()) and self.tf_listener.canTransform('landmark3', 'map', rospy.Time.now()):
        #         break

        while not rospy.is_shutdown():
            # print("aaaaaaaaaa")
            pass

    def geometry_validation(self, mpost1, mpost2, mpost3):
        mdis23 = mpost2.distanceto(mpost3)
        mdis12 = mpost1.distanceto(mpost2)
        mdis13 = mpost1.distanceto(mpost3)
        # SSS
        if abs(mdis12 - mdis13) < 0.2:
            return 1
        elif abs(mdis12 - self.landmark1.distanceto(self.landmark2)) < self.sss_equiv_threshold and abs(mdis13 - self.landmark1.distanceto(self.landmark3)) < self.sss_equiv_threshold and abs(mdis23 - self.landmark2.distanceto(self.landmark3)) < self.sss_equiv_threshold:
            return 1
        else:
            return 0

    def output_validation(self, output_pose):
        if self.tf_listener.canTransform('map', 'base_footprint', rospy.Time(0)):
            bf = self.tf_listener.lookupTransform('map', 'base_footprint', rospy.Time(0))
            (roll, pitch, yaw) = euler_from_quaternion(bf[1])
            bf = pose(bf[0][0], bf[0][1], yaw)
            if bf.distanceto(output_pose) > 0.5:
                return 0
            else:
                return 1

    def landmark_extraction(self, raw_obsList):
        tf1_success = 0
        tf2_success = 0
        tf3_success = 0
        if self.tf_listener.canTransform('base_footprint', 'landmark1', rospy.Time(0)):
            bf_landmark1 = self.tf_listener.lookupTransform('base_footprint', 'landmark1', rospy.Time(0))
            bf_landmark1 = pose(bf_landmark1[0][0], bf_landmark1[0][1], 0)
            tf1_success = 1
        if self.tf_listener.canTransform('base_footprint', 'landmark2', rospy.Time(0)):
            bf_landmark2 = self.tf_listener.lookupTransform('base_footprint', 'landmark2', rospy.Time(0))
            bf_landmark2 = pose(bf_landmark2[0][0], bf_landmark2[0][1], 0)
            tf2_success = 1
        if self.tf_listener.canTransform('base_footprint', 'landmark3', rospy.Time(0)):
            bf_landmark3 = self.tf_listener.lookupTransform('base_footprint', 'landmark3', rospy.Time(0))
            bf_landmark3 = pose(bf_landmark3[0][0], bf_landmark3[0][1], 0)
            tf3_success = 1
        if tf1_success and tf2_success and tf3_success:
            min_err1 = 10000000000
            min_err2 = 10000000000
            min_err3 = 10000000000
            lm1_extracted = pose(0,0,0)
            lm2_extracted = pose(0,0,0)
            lm3_extracted = pose(0,0,0)
            lm1_captured = 0
            lm2_captured = 0
            lm3_captured = 0
            for obs in raw_obsList:
                err1 = obs.distanceto(bf_landmark1)
                err2 = obs.distanceto(bf_landmark2)
                err3 = obs.distanceto(bf_landmark3)
                if err1 < self.landmark_extraction_threshold:
                    if err1 < min_err1:
                        min_err1 = err1
                        lm1_extracted = obs
                        lm1_captured = 1
                if err2 < self.landmark_extraction_threshold:
                    if err2 < min_err2:
                        min_err2 = err2
                        lm2_extracted = obs
                        lm2_captured = 1
                if err3 < self.landmark_extraction_threshold:
                    if err3 < min_err3:
                        min_err3 = err3
                        lm3_extracted = obs
                        lm3_captured = 1
            if lm1_captured and lm2_captured and lm3_captured:
                return [lm1_extracted, lm2_extracted, lm3_extracted]
            else:
                return "Not found"
        else:
            return "Not found"

    def trilateration(self, scanList, landmarkList):
        if len(scanList) == 3:
            #-------------------identify scan data-----------------------#
            comb = itertools.combinations(scanList, 2)
            d_lm23 = 100000000000
            for i in comb:
                dis = i[0].distanceto(i[1])
                if dis < d_lm23:
                   d_lm23 = dis
                   m_landmark23 = i

            for i in scanList:
                if i != m_landmark23[0] and i != m_landmark23[1]:
                    m_landmark1 = i            
            
            side23 = vector(m_landmark23[0], m_landmark23[1])
            vec_1mid = vector(m_landmark1, side23.mid_point())
            unit_vec_1mid = vec_1mid.unit_vector()
            unit_vec_mid2 = unit_vec_1mid.rotate(-pi/2)
            unit_vec_mid3 = unit_vec_1mid.rotate(pi/2)
            est_landmark2 = pose(side23.mid_point().x + 0.5*side23.length()*unit_vec_mid2.d_x, side23.mid_point().y + 0.5*side23.length()*unit_vec_mid2.d_y, 0)
            est_landmark3 = pose(side23.mid_point().x + 0.5*side23.length()*unit_vec_mid3.d_x, side23.mid_point().y + 0.5*side23.length()*unit_vec_mid3.d_y, 0)

            for i in m_landmark23:
                if est_landmark2.distanceto(i) < 0.5:
                    m_landmark2 = i
                if est_landmark3.distanceto(i) < 0.5:
                    m_landmark3 = i
            #------------------------------------------------------------#
            if self.geometry_validation(m_landmark1, m_landmark2, m_landmark3):
            # if 1:
                r1 = m_landmark1.distanceto(pose(0,0,0))
                r2 = m_landmark2.distanceto(pose(0,0,0))
                r3 = m_landmark3.distanceto(pose(0,0,0))
                m_side23 = m_landmark2.distanceto(m_landmark3)
                if m_side23 > 0.001:
                # print ("m_side23 = "), m_side23
                    len_y = (pow(r2, 2)-pow(r3, 2)+pow(m_side23,2))/2/m_side23
                    cur_x = self.landmark2.x - (math.sqrt(pow(r2,2)-pow(len_y,2)))
                    cur_y = len_y + self.landmark2.y
                    vec32 = vector(m_landmark3, m_landmark2)
                    unit_vec32 = vec32.unit_vector()
                    cur_theta = math.acos(unit_vec32.d_x/1)
                    if m_landmark2.y > m_landmark3.y:
                        cur_theta *= -1
                    cur_theta = self.theta_convert(cur_theta - pi/2)
                    print("current robot pose at :"), (round(cur_x,4), round(cur_y,4), round(math.degrees(cur_theta),4))
                    if self.output_validation(pose(cur_x, cur_y, cur_theta)):
                        self.pose_publish(cur_x,cur_y,cur_theta)
                        print("pose published ")

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

    def pose_publish(self,x,y,theta):
        pos_msg = PoseWithCovarianceStamped()
        pos_msg.header.frame_id = "map"
        pos_msg.header.stamp = rospy.get_rostime()
        pos_msg.pose.pose.position.x = x
        pos_msg.pose.pose.position.y = y
        pos_msg.pose.pose.position.z = 0
        q = quaternion_from_euler(0,0,theta)
        pos_msg.pose.pose.orientation.x = q[0]
        pos_msg.pose.pose.orientation.y = q[1]
        pos_msg.pose.pose.orientation.z = q[2]
        pos_msg.pose.pose.orientation.w = q[3]
        pos_msg.pose.covariance = [0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
                                   0.0, 0.1, 0.0, 0.0, 0.0, 0.0,
                                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                   0.0, 0.0, 0.0, 0.0, 0.0, 0.1]
        self.posePub.publish(pos_msg)

    def show_landmark_extracted(self, landmarks):
        msg = Obstacles()
        msg.header.stamp = rospy.Time(0)
        msg.header.frame_id = "base_footprint"
        circleList = []
        
        for i in landmarks:
            circle = CircleObstacle()
            circle.center.x = i.x
            circle.center.y = i.y
            circle.radius = 0.15
            circle.true_radius = 0.1
            circleList.append(circle)
        msg.circles = circleList
        self.landmark_rviz.publish(msg)
        
if __name__ == '__main__':
    try:
        rospy.init_node('lidar_localization', anonymous = True)
        getPose = localization()
        getPose.init()
    except rospy.ROSInterruptException:
        pass
