#ifndef PLANNER_STATE_H_
#define PLANNER_STATE_H_
//ros
#include <ros/ros.h>
#include <std_msgs/Int32MultiArray.h>
#include <geometry_msgs/PoseStamped.h>
#include <tf2/LinearMath/Quaternion.h>
//c++
#include <string>
#include <vector>
//my lib

#define P_NUM 3  //planner_mission的數量 : 1.x 2.y 3.theta

using namespace std;

class PlannerManager{
public:
  PlannerManager();
  ~PlannerManager(){};

  void get_state(); //update msg and check if navigation complete the mission
  void P_callback(const std_msgs::Int32MultiArray::ConstPtr&);
  void executing(double,double,double);
  bool ifcomplete(int); //return if navigation complete or not

private:
  ros::NodeHandle n;
  ros::Publisher planner_pub; //pub goal to navigation
  ros::Subscriber planner_sub; //sub form navigation, get navigation status

  tf2::Quaternion odom_quat;
  geometry_msgs::PoseStamped transformStamped;

  vector<int> p_state; //[0] 到點與否  , [1] 找到路徑與否 , [2] count
  int last_count; // for msg count
  bool nav_getMission;
  bool m_complete; // check if mission is complete
  int complete_count;
};

#endif