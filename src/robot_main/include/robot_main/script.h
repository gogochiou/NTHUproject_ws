#ifndef SCRIPT_H_
#define SCRIPT_H_

//ros
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32.h>
//c++
#include <stdlib.h>
#include <string>
//my lib
#include <robot_main/getMission.h> //srv for main and gui


using namespace std;

class Script;

class mission{
  friend class Script;
public:
  mission(){};
  mission(int, double, double, double, string, string);
  ~mission(){};

private:
  int order; //mission number 順序
  double x;
  double y;
  double theta;
  string action; //Grab, Release, Hold
  string color;
};

class Script{
public:
  Script();
  ~Script(){};
  void readfile(); // if need, read from excel file
  void refresh();  // refresh by gui
  bool getMission(int num_); //read target mission from gui 
  void missionComplete(); //tell gui all mission is complete
  void gui_sub_callback(const std_msgs::String::ConstPtr&);
  void mCount_sub_callback(const std_msgs::Int32::ConstPtr&);

  //return value
  double* get_missionPose();
  string* get_missionAct();
  int get_m_quantity(){return mission_number; };

private:
  ros::NodeHandle n;
  ros::Subscriber gui_sub;
  ros::Subscriber mCount_sub;
  ros::ServiceClient mission_client;

  bool r_file; // read excel file or not
  bool r_gui;  // read script from gui
  bool tell_;  // tell gui mission complete
  int mission_number; // 任務數量
  mission* mList;
  mission* m_return; 
  
};


#endif