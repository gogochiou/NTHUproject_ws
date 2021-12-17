#include <ros/ros.h>
#include <robot_main/script.h>

using namespace std;

#define P_NUM 3
#define A_NUM 2

mission::mission(int num_, double x_, double y_, double theta_, string action_, string color_){
  order = num_;
  x = x_;
  y = y_;
  theta = theta_;
  action = action_;
  color = color_;
}

Script::Script(){
  ros::NodeHandle nh("~");
  gui_sub = n.subscribe<std_msgs::String>("script_update",10,&Script::gui_sub_callback,this);
  mCount_sub = n.subscribe<std_msgs::Int32>("mission_count",10,&Script::mCount_sub_callback,this);
  mission_client = n.serviceClient<robot_main::getMission>("get_mission");

  nh.param("read_excel",r_file,false);
  nh.param("use_gui",r_gui,false);
  tell_ = false;

  if(r_file)
    readfile();
  else if(r_gui){
    //read script from gui
  }
  else{
    // setting script
    XmlRpc::XmlRpcValue script_;
    nh.param("mission_number",mission_number,4);
    nh.param("mission_script",script_,script_);

    mList = new mission[mission_number];
    for(int i=0;i<mission_number;i++){
      XmlRpc::XmlRpcValue mission_ = script_[i];
      mList[i].order = i;
      mList[i].x = mission_[0];
      mList[i].y = mission_[1];
      mList[i].theta = mission_[2];
      mList[i].action = string(mission_[3]);
      mList[i].color = string(mission_[4]);

      //Show input mission
      ROS_INFO_STREAM("Mission "<<i);
      ROS_INFO_STREAM("  x pos : "<<mList[i].x);
      ROS_INFO_STREAM("  y pos : "<<mList[i].y);
      ROS_INFO_STREAM("  theta : "<<mList[i].theta);
      ROS_INFO_STREAM("  act   : "<<mList[i].action);
      ROS_INFO_STREAM("  color : "<<mList[i].color);
      ROS_INFO("-----------------------------------------");
    }
  }
  //update info from gui
  refresh();

}

void Script::readfile(){
  ROS_INFO("Reading......");
}

void Script::refresh(){
  ros::spinOnce();
}

bool Script::getMission(int num_){ //其實可以用void就好，只是測試時可以看true false
  if(!r_gui){
    m_return = new mission(mList[num_].order, mList[num_].x, mList[num_].y, mList[num_].theta,
                           mList[num_].action, mList[num_].color);
    return true;
  }
  robot_main::getMission srv;
  srv.request.m_num = num_;
  if(mission_client.call(srv)){
    m_return = new mission(num_, srv.response.x, srv.response.y, srv.response.theta,
                           srv.response.action, srv.response.color);
    if(m_return->action == "End")
      return false;
    else
      return true;
  }
  else{
    // ROS_INFO_STREAM("Searching for mission");
    return getMission(num_);
  }
}

void Script::missionComplete(){
  robot_main::getMission srv;
  srv.request.m_num = mission_number;
  if(!tell_&&mission_client.call(srv))
    tell_ = true;
  return;
}

void Script::gui_sub_callback(const std_msgs::String::ConstPtr& msg){
  if(r_gui)
    return;
  for (int i = 0; i < mission_number; i++){
    if(mList[i].action == "Grab"){
      mList[i].color = msg->data;
      ROS_INFO("Mission %d is set to color %s", i, mList[i].color.c_str());
    }
  }
}

void Script::mCount_sub_callback(const std_msgs::Int32::ConstPtr& msg){
  if(!r_gui)
    return;
  mission_number = msg->data;
  mList = new mission[mission_number];
  ROS_INFO_STREAM("Get Mission num : "<<mission_number);
}

double* Script::get_missionPose(){
  double* pose_arr = new double[P_NUM]; // local array can not be return, but use "new" can solve this?
  pose_arr[0] = m_return->x;
  pose_arr[1] = m_return->y;
  pose_arr[2] = m_return->theta;
  return pose_arr;
}

string* Script::get_missionAct(){
  string* act_arr = new string[A_NUM];
  act_arr[0] = m_return->action;
  act_arr[1] = m_return->color;
  return act_arr;
}