#include <ros/ros.h>
#include <std_msgs/String.h>
#include <string>

using namespace std;

string command;

void invoke_callback(const std_msgs::String::ConstPtr& msg){
  ROS_INFO("I get somthing new");
  command = msg->data;
}

int main(int argc, char **argv){
  ros::init(argc, argv, "invoke_camera");
  ros::NodeHandle n;

  ros::Subscriber invoke_sub = n.subscribe<std_msgs::String>("camera_invoke",50,invoke_callback);

  bool open = false;
  command = "No";
  
  ros::Rate rate(100);  
  while (ros::ok()){
    ros::spinOnce();
    if(command == "Invoke" && !open){
      open=true;
      ROS_INFO("Open node");
      system("roslaunch pcl pcl.launch");
    }
    ROS_INFO("Not going to open anything");
    rate.sleep();
  }
  return 0;
}