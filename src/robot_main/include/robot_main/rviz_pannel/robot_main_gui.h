#ifndef ROBOT_GUI_H
#define ROBOT_GUI_H

#include <ros/ros.h>
#include <rviz/panel.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32.h>
#include <robot_main/main2arm.h> //msg for camera
#include <robot_main/getMission.h> //srv for main and gui
//c++
#include <string.h>

// Qt
#include <QLabel>
#include <QFrame>
#include <QCheckBox>
#include <QLineEdit>
#include <QButtonGroup>
#include <QPushButton>
#include <QRadioButton>
#include <QGroupBox>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QMessageBox>
#include <QStandardItemModel>
#include <QItemSelectionModel>
#include <QTableView>
#include <QHeaderView>
#include <QStyle>
#include <QDebug>

using namespace std;

namespace robot_main{
class robot_gui: public rviz::Panel{
Q_OBJECT
public:
  robot_gui(QWidget* parent=0);
  virtual void load( const rviz::Config& config );
  virtual void save( rviz::Config config )const;
  void getScript();
  void sendState();//send state and color
  void sendColor2camera(string); //only for demo camera
  bool return_mission(robot_main::getMission::Request &req,robot_main::getMission::Response &res);
  void setRPose(XmlRpc::XmlRpcValue);//set Release Pose
  void change_mission_color();
  void change_release_pose();

private Q_SLOTS:
  void processCheck();//check if open gui
  void ready_click();
  void start_click();
  void restart_click();
  void setColor();
  void removeMission();
  void addMission();

private:
  QCheckBox* activate_checkbox_;
  //setting
  QButtonGroup* color_group_;
  QRadioButton* red_button_;
  QRadioButton* green_button_;
  QRadioButton* blue_button_;
  QPushButton* ready_button_;
  QPushButton* start_button_;
  QPushButton* restart_button_;
  //script
  QStandardItemModel* script_;
  QTableView* script_table_;
  QPushButton* remove_button_;
  QLineEdit* x_input_;
  QLineEdit* y_input_;
  QLineEdit* theta_input_;
  QLineEdit* action_input_;
  QLineEdit* color_input_;
  QPushButton* add_button_;
  QPushButton* clear_button_;
  
  //Ros
  ros::NodeHandle nh_,nh_local_;
  ros::Publisher state_pub, color_pub;
  ros::Publisher camera_pub;
  ros::Publisher mCount_pub; //pub total number of mission in script
  ros::ServiceServer m_server;

  //param
  string r_state_;
  string color_;
  XmlRpc::XmlRpcValue r_Rpose_,g_Rpose_,b_Rpose_;//color_ReleasePose
  QString ReleasePose_;
  int column_number_;
  bool p_active_;
  bool send2camera_; // send message to camera for demo
  bool gui_sendScript_; //use gui to send mission to main
  bool threeReleaseMission_; //if there is three different pose for Release cube due to unique color

};

}// namespace robot_main

#endif