#include <ros/ros.h>
#include <robot_main/gui_state.h>

GUI::GUI(){
  gui_sub = n.subscribe<std_msgs::String>("update_status",10,&GUI::gui_sub_callback,this);
}

void GUI::update(Robot* robot_){
  ros::spinOnce();
  if(robot_->status == Status::Run){ //其實這個有點多餘哈哈
    ROS_INFO("Not able to input command from GUI, cause robot status is Run");
    return;
  }
  if(desire_state == "Run"){
    if(robot_->status == Status::End) //when status is end, need reset(ready) first
      return;
    robot_->status = Status::Run;
  }
  else if(desire_state == "Ready"){
    robot_->status = Status::Ready;
  }
  else if(desire_state == "Restart"){
    //need to 初始化所有數值
    robot_->status = Status::Setting;
  }
}


void GUI::gui_sub_callback(const std_msgs::String::ConstPtr& msg){
  desire_state = msg->data;
}