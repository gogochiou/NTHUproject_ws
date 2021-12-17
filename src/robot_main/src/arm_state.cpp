#include <ros/ros.h>
#include <ros/master.h>
#include <robot_main/arm_state.h>

using namespace std;

ArmManager::ArmManager(){
  arm_pub = n.advertise<robot_main::main2arm>("arm_mission", 1);
  arm_sub = n.subscribe<robot_main::arm2main>("arm_to_main", 1, &ArmManager::A_callback, this);
  
  //init param
  a_state = {"Hold","Success"};
  a_command.action = "Hold";
  a_command.color = "No";
  Arm_getMission = false;
  complete_count = -1;
  redo_flag = false;
  redo_count = 0;
  if_count = false;
}

void ArmManager::get_state(string action_){
  ros::spinOnce();
  // if(!if_count){
  //   ROS_INFO_STREAM("ARM complete count(inside) : "<<complete_count);
  //   Arm_getMission = false;
  //   return;
  // }
  if(a_state[0] == "Hold"){
    Arm_getMission = false;
    return;
  }
  if(action_!=a_state[0]){
    Arm_getMission = false;
    return;
  }

  if(Arm_getMission && a_state[1]=="Success"){
    ROS_INFO("ARM get success");
    ROS_INFO_STREAM("ARM complete count : "<<complete_count);
    complete_count++;
    Arm_getMission = false;
    // if_count = false;
  }
  else if(Arm_getMission && a_state[1]=="Fail"){
    redo_count++;
    if(redo_count>3){
      redo_count = 0;
      complete_count++;
      ROS_INFO("Skip the Mission, We have try 3 times");
    }
    Arm_getMission = false;
  }
}

void ArmManager::A_callback(const robot_main::arm2main::ConstPtr& msg){
  if(a_command.action==msg->action){
    Arm_getMission = true;
    a_state[0]=msg->action;
    a_state[1]=msg->situation;
  }
  else
    ROS_INFO("Arm mission action is not match !");

}

void ArmManager::executing(string action_, string color_, bool count){
  if_count = count;
  if(action_ =="Hold"){
    complete_count++;
    Arm_getMission = false;
    return;
  }
  // if(redo_flag){
  //   pub_command("Hold","No");
  //   ROS_INFO("Redoing Hold works");
  // }
  else{
    pub_command(action_,color_);
  }
}

void ArmManager::pub_command(string action_, string color_){
  ROS_INFO_STREAM("ARM get mission : "<<Arm_getMission);
  ROS_INFO_STREAM("ARM complete count(execute) : "<<complete_count);
  if(Arm_getMission)
    return;

  if(action_=="Grab"&&color_!="No"){
    while(arm_pub.getNumSubscribers()<2){
      ROS_INFO("Waiting for camera node open . Subscriber : %d",arm_pub.getNumSubscribers());
    }
  }
  ROS_INFO_STREAM("There is two person or more subscribe me");
  a_command.action = action_;
  a_command.color = color_;
  arm_pub.publish(a_command);
}

bool ArmManager::ifcomplete(int m_num){
  if(m_num!=complete_count){
    ROS_INFO("Arm works on mission %d",m_num);
    return false;
  }
  else{
    ROS_INFO("Arm completes mission %d",complete_count); 
    return true;
  }
}