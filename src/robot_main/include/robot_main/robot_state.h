#ifndef ROBOT_STATE_H_
#define ROBOT_STATE_H_
//ros
#include <ros/ros.h>
#include <std_msgs/String.h>
//c++
#include <string>
//my lib
#include <robot_main/arm_state.h>
#include <robot_main/planner_state.h>

using namespace std;

enum Status {Setting,Refresh,Run,Ready,End};

class GUI;

class Robot{
  friend class GUI;
public:
  Robot();
  ~Robot(){};
  void SWstatus(Status);
  Status get_status(int); //get robot status
  void show_mission(double*,string*);
  void execute_mission(int,double*,string*,bool);

  //for return value
  int mission_count(){return m_count; };

private:
  //部份加入指標，是因為cmake編譯上會找不到宣告的類別，所以不能宣告為實體
  ros::NodeHandle n;
  ros::Publisher invoke_pub;//tell invoke_camera node to make it open camera
  Status status;
  GUI* gui;
  PlannerManager planner;     //for arm
  ArmManager arm; //for navigation

  int m_count; //executed mission number
  bool camera_open;
};

#endif