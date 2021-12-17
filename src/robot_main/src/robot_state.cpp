#include <ros/ros.h>
#include <robot_main/robot_state.h>
#include <robot_main/gui_state.h>

using namespace std;

Robot::Robot(){
  invoke_pub = n.advertise<std_msgs::String>("camera_invoke",1);
  gui = new GUI();

  status = Status::Setting;
  m_count = 0;
}

void Robot::SWstatus(Status new_status){
  status = new_status;
}

Status Robot::get_status(int m_quantity_){
  //if robot is running , there is no need to get the msg from gui
  if(status == Status::Run){
    // 檢查是否完成所有任務
    if(m_count >= m_quantity_){
      status = Status::End;
    }
    return status;
  }
  
  gui->update(this);
  return status;
}

void Robot::show_mission(double* d_pose,string* d_act){
  ROS_INFO("Current Mission :");
  ROS_INFO(" Pos - x : %lf, y : %lf, theta : %lf ", d_pose[0],d_pose[1],d_pose[2]);
  ROS_INFO(" Arm - action : %s, color : %s",d_act[0].c_str(),d_act[1].c_str());
}

void Robot::execute_mission(int m_number,double* d_pose,string* d_act,bool simultaneously){
  show_mission(d_pose, d_act);
  planner.get_state();
  arm.get_state(d_act[0]);
  if(simultaneously){
    //simultaneously operate planner and arm
  }
  else{
    if(!planner.ifcomplete(m_number)){
      //execute
      planner.executing(d_pose[0],d_pose[1],d_pose[2]);
      // arm.executing("Hold","No",false);
    }
    else if(!arm.ifcomplete(m_number)){//check if complete
      //open camera
      if(d_act[0]=="Grab" && d_act[1]!="No"){
        std_msgs::String output;
        output.data = "Invoke";
        invoke_pub.publish(output);
      }
      else{
        std_msgs::String output;
        output.data = "No";
        invoke_pub.publish(output);
      }

      //execute
      arm.executing(d_act[0],d_act[1],true);
    }
    else{
      //kill camera node
      if(d_act[0]=="Grab"){
        system("rosnode kill camera/color_rectify_color"); 
        system("rosnode kill camera/points_xyzrgb_hw_registered");
        system("rosnode kill camera/realsense2_camera");
        system("rosnode kill camera/realsense2_camera_manager");
        system("rosnode kill segmentation");
        system("rosnode kill camera_base_tf");
      }
      //change next mission
      m_count++;
    }
  }
}