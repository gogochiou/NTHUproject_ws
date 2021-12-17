#!/usr/bin/env python

import rospy
from kivymd.app import MDApp
from kivy.lang import Builder

if __name__ == '__main__':
  rospy.init_node('robot_gui',anonymous=True)