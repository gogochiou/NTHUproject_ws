#ifndef GUI_STATE_H_
#define GUI_STATE_H_
//ros
#include <ros/ros.h>
#include <std_msgs/String.h>
//c++
#include <stdlib.h>
#include <string>
//my lib
#include <robot_main/robot_state.h>

using namespace std;

class GUI{
public:
  GUI();
  ~GUI(){};
  void update(Robot*);
  void gui_sub_callback(const std_msgs::String::ConstPtr&);

private:
  ros::NodeHandle n;
  ros::Subscriber gui_sub;

  string desire_state; // desire main state -> Restart, Run, Ready
};

#endif