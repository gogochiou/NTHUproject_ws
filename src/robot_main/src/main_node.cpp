#include <ros/ros.h>
#include <robot_main/script.h>
#include <robot_main/robot_state.h>
#include <robot_main/gui_state.h>

#include <string>

using namespace std;

int main(int argc, char **argv){
  ros::init(argc, argv, "main_node");
  ros::NodeHandle n;
  Script script;
  Robot robot;

  int m_count = 0;
  int m_quantity = 0;
  double* d_pose;//get from script, desire mission pose
  string* d_act; //get from script, desire mission action

  ros::Rate rate(100);

  while(ros::ok()){
    switch(robot.get_status(m_quantity)){
      case Status::Setting:
        ROS_INFO("Robot Status : Setting");
        break;
      case Status::Ready:
        ROS_INFO("Robot Status : Ready");
        m_quantity = script.get_m_quantity();//get total mission count
        ROS_INFO_STREAM("Total mission : "<<m_quantity);
        break;
      case Status::Run:
        ROS_INFO("Robot Status : Run");
        m_count = robot.mission_count();
        script.getMission(m_count);
        d_pose = script.get_missionPose();
        d_act = script.get_missionAct();
        robot.execute_mission(m_count, d_pose, d_act, false);
        
        break;
      case Status::End:
        script.missionComplete();
        ROS_INFO("Robot Status : End");
        break;
    }

    ROS_INFO("---------");
    rate.sleep();
  }

  return 0;
}
