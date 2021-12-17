#include <ros/ros.h>
#include "robot_main/rviz_pannel/robot_main_gui.h"

using namespace robot_main;

int main(int argc, char** argv) {
  ros::init(argc, argv, "gui_param_node", ros::init_options::NoRosout);
  ros::NodeHandle nh("");
  ros::NodeHandle nh_local("~");

  try {
    ROS_INFO("[Gui Param]: Setting param !");
    ros::spin();
  }
  catch (const char* s) {
    ROS_FATAL_STREAM("[Gui Param]: " << s);
  }
  catch (...) {
    ROS_FATAL_STREAM("[Gui Param]: Unexpected error");
  }

  return 0;
}