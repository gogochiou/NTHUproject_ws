#ifndef ARM_STATE_H_
#define ARM_STATE_H_
//ros
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <robot_main/main2arm.h>
#include <robot_main/arm2main.h>
//c++
#include <string>
#include <vector>
//my lib

#define A_NUM 2  //arm_mission的數量 : 1.action 2.color 

using namespace std;

class ArmManager{
public:
  ArmManager();
  ~ArmManager(){};
  void get_state(string);
  void A_callback(const robot_main::arm2main::ConstPtr&);
  void executing(string, string, bool);
  void pub_command(string, string);
  bool ifcomplete(int);

private:
  ros::NodeHandle n;
  ros::Publisher arm_pub; //pub work mission to arm
  ros::Subscriber arm_sub; //sub form arm, get arm status

  vector<string> a_state; //arm to main
  robot_main::main2arm a_command;

  bool Arm_getMission;
  int complete_count; // count for mission that is complete
  bool redo_flag;    //check if need to redo(republish command one times)
  int redo_count;    //check redo how many times (per mission)
  bool if_count; // if planner is work, than complete count cannot add 

  
};

#endif