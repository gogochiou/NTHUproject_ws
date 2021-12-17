#include <ros/ros.h>
#include <robot_main/planner_state.h>

using namespace std;

PlannerManager::PlannerManager(){
  planner_pub = n.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal", 1000);
  planner_sub = n.subscribe<std_msgs::Int32MultiArray>("plan_state", 10, &PlannerManager::P_callback, this);

  p_state = {1,0,0};
  last_count = 0;
  nav_getMission = false;
  m_complete = false;
  complete_count = -1;
}

void PlannerManager::get_state(){
  last_count = p_state[2];
  ros::spinOnce();
  //add check if goal can be reach?

  if(p_state[0]==1 && last_count<p_state[2] && nav_getMission){//check if complete mission
    ROS_INFO_STREAM("Planner complete count : "<<complete_count);
    complete_count++;
    nav_getMission = false;
  }
}

void PlannerManager::P_callback(const std_msgs::Int32MultiArray::ConstPtr& msg){
  if(msg->data[2]!=last_count ){ // check if a new message
    nav_getMission = true;
    p_state.assign(msg->data.begin(), msg->data.end());
      
  }
}

void PlannerManager::executing(double x,double y,double theta){
  if(m_complete || nav_getMission)//only pub when mission not complete and navigation did not get msg
    return;

  transformStamped.header.stamp = ros::Time::now();
  transformStamped.header.frame_id = "map";

  transformStamped.pose.position.x = x;
  transformStamped.pose.position.y = y;
  transformStamped.pose.position.z = 0;
  odom_quat.setRPY(0, 0, theta);
  transformStamped.pose.orientation.x = odom_quat.x();
  transformStamped.pose.orientation.y = odom_quat.y();
  transformStamped.pose.orientation.z = odom_quat.z();
  transformStamped.pose.orientation.w = odom_quat.w();
  ROS_INFO("PlannerManager publish goal!");
  planner_pub.publish(transformStamped);
  nav_getMission = true;
}

bool PlannerManager::ifcomplete(int m_num){//return if complete
  if(m_num!=complete_count){
    ROS_INFO("Planner works on mission %d",m_num);
    m_complete = false;
    return false;
  }
  else{
    ROS_INFO("Planner completes mission %d",m_num); 
    m_complete = true;
    return true;
  }
}