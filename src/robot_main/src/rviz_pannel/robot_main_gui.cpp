#include <ros/ros.h>
#include <robot_main/rviz_pannel/robot_main_gui.h>

using namespace robot_main;
using namespace std;

robot_gui::robot_gui(QWidget* parent):rviz::Panel(parent),nh_local_("gui_param_node"){
  state_pub = nh_.advertise<std_msgs::String>("update_status",10);
  color_pub = nh_.advertise<std_msgs::String>("script_update",10);
  camera_pub = nh_.advertise<robot_main::main2arm>("arm_mission",10);
  mCount_pub = nh_.advertise<std_msgs::Int32>("mission_count",10);
  m_server = nh_.advertiseService("get_mission",&robot_gui::return_mission,this);
  r_state_ = "Setting";
  color_ = "No";
  column_number_ = 3;//may be a param

  //read param (basic)
  nh_local_.param<bool>("active",p_active_,true);
  nh_local_.param<bool>("camera_demo",send2camera_,false);
  nh_local_.param<bool>("gui_send_script",gui_sendScript_,false);
  //read param of 3 type of position (Release cube mission)
  nh_local_.param<bool>("threeReleaseMission",threeReleaseMission_,false);
  nh_local_.param("Red_ReleasePose",r_Rpose_,r_Rpose_);
  nh_local_.param("Green_ReleasePose",g_Rpose_,g_Rpose_);
  nh_local_.param("Blue_ReleasePose",b_Rpose_,b_Rpose_);

  activate_checkbox_ = new QCheckBox("On/Off");
  red_button_ = new QRadioButton(tr("Red"));
  green_button_ = new QRadioButton(tr("Green"));
  blue_button_ = new QRadioButton(tr("Blue"));
  ready_button_ = new QPushButton("Ready");
  start_button_ = new QPushButton("Start");
  restart_button_ = new QPushButton("Restart");
  script_ = new QStandardItemModel();
  remove_button_ = new QPushButton("Remove Mission");
  x_input_ = new QLineEdit();
  y_input_ = new QLineEdit();
  theta_input_ = new QLineEdit();
  action_input_ = new QLineEdit();
  color_input_ = new QLineEdit();
  add_button_ = new QPushButton("Add Mission");
  clear_button_ = new QPushButton("Clear");

  /* setting gui interface */
  //line type
  QFrame* lines[2];
  for (auto& line : lines) {
    line = new QFrame();
    line->setFrameShape(QFrame::HLine);
    line->setFrameShadow(QFrame::Sunken);
  }

  // margin to box edge
  QSpacerItem* margin = new QSpacerItem(1, 1, QSizePolicy::Expanding, QSizePolicy::Fixed);

  //1.Part of "setting"
  QGridLayout* setting_layout = new QGridLayout;
  //color select
  color_group_ = new QButtonGroup(this);
  color_group_->addButton(red_button_,0);
  color_group_->addButton(green_button_,1);
  color_group_->addButton(blue_button_,2);
  // red_button_->setChecked(true);
  int count=0;
  QList<QAbstractButton*> buttonList=color_group_->buttons();
  for(QList<QAbstractButton*>::const_iterator it=buttonList.cbegin(); it!=buttonList.cend(); ++it){
    setting_layout->addWidget(*it,count,0);
    count++;
  }
  //state select
  setting_layout->addWidget(ready_button_,count,0);
  setting_layout->addWidget(start_button_,count,1);
  setting_layout->addWidget(restart_button_,count,2);

  QGroupBox* setting_box = new QGroupBox("Setting");
  setting_box->setLayout(setting_layout);

  //2.Part of script
  script_->setColumnCount(3);
  script_->setHorizontalHeaderItem(0,new QStandardItem(QString("X,Y,Theta")));
  script_->setHorizontalHeaderItem(1,new QStandardItem(QString("Action")));
  script_->setHorizontalHeaderItem(2,new QStandardItem(QString("Color")));
  // script_->setVerticalHeaderLabels();
  getScript(); //read script param

  script_table_ = new QTableView;
  script_table_->setModel(script_);
  script_table_->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch); //adaptive width
  script_table_->verticalHeader()->hide();
  script_table_->setSelectionBehavior(QAbstractItemView::SelectRows);
  script_table_->setSelectionMode(QAbstractItemView::MultiSelection);

  QHBoxLayout* xytheta_layout = new QHBoxLayout;
  xytheta_layout->addWidget(new QLabel("X:"));
  xytheta_layout->addWidget(x_input_);
  xytheta_layout->addWidget(new QLabel("Y:"));
  xytheta_layout->addWidget(y_input_);
  xytheta_layout->addWidget(new QLabel("Theta:"));
  xytheta_layout->addWidget(theta_input_);

  QHBoxLayout* ac_layout = new QHBoxLayout;
  ac_layout->addWidget(new QLabel("Action:"));
  ac_layout->addWidget(action_input_);
  ac_layout->addWidget(new QLabel("Color:"));
  ac_layout->addWidget(color_input_);

  QHBoxLayout* m_button_layout = new QHBoxLayout;
  m_button_layout->addWidget(clear_button_);
  m_button_layout->addWidget(add_button_);

  QVBoxLayout* script_set = new QVBoxLayout;
  script_set->addWidget(script_table_);
  script_set->addWidget(remove_button_);
  script_set->addLayout(xytheta_layout);
  script_set->addLayout(ac_layout);
  script_set->addLayout(m_button_layout);

  QGroupBox* script_set_box = new QGroupBox("Script");
  script_set_box->setLayout(script_set);

  //3.Part of merge(all)
  QVBoxLayout* total_layout = new QVBoxLayout;
  total_layout->addWidget(activate_checkbox_);
  total_layout->addWidget(lines[0]);
  total_layout->addWidget(setting_box);
  total_layout->addWidget(script_set_box);
  total_layout->addStretch(); //使下面多了空白的空間，而不是用上面的box填滿
  // total_layout->setAlignment(total_layout, Qt::AlignCenter);
  setLayout(total_layout);

  connect( activate_checkbox_, SIGNAL(clicked()), this, SLOT(processCheck()) );
  connect( red_button_,SIGNAL(clicked()),this,SLOT(setColor()) );
  connect( green_button_,SIGNAL(clicked()),this,SLOT(setColor()) );
  connect( blue_button_,SIGNAL(clicked()),this,SLOT(setColor()) );
  connect( ready_button_,SIGNAL(clicked()),this,SLOT(ready_click()) );
  connect( start_button_,SIGNAL(clicked()),this,SLOT(start_click()) );
  connect( restart_button_,SIGNAL(clicked()),this,SLOT(restart_click()) );
  connect( remove_button_,SIGNAL(clicked()),this,SLOT(removeMission()));
  connect( add_button_,SIGNAL(clicked()),this,SLOT(addMission()));

  //init the process
  activate_checkbox_->setChecked(p_active_);
  processCheck();
}

void robot_gui::processCheck(){
  p_active_ = activate_checkbox_->isChecked();
  red_button_->setEnabled(p_active_);
  green_button_->setEnabled(p_active_);
  blue_button_->setEnabled(p_active_);
  ready_button_->setEnabled(p_active_);
  start_button_->setEnabled(p_active_);
  restart_button_->setEnabled(p_active_);

  x_input_->setEnabled(p_active_);
  y_input_->setEnabled(p_active_);
  theta_input_->setEnabled(p_active_);
  action_input_->setEnabled(p_active_);
  color_input_->setEnabled(p_active_);
  add_button_->setEnabled(p_active_);
  clear_button_->setEnabled(p_active_);
  remove_button_->setEnabled(p_active_);
  
}

void robot_gui::ready_click(){
  r_state_ = "Ready";
  sendState();
}

void robot_gui::start_click(){
  if(r_state_ != "Ready"){
    QMessageBox::warning(NULL,"Warning","Setting has not been done",QMessageBox::Ok,QMessageBox::Ok);
    return;
  }
  r_state_ = "Run";
  ready_button_->setEnabled(false);
  sendState();
}

void robot_gui::restart_click(){
  r_state_ = "Restart";
  color_ = "No";
  // back to initial set
  QAbstractButton* checked = color_group_->checkedButton();
  if (checked){
    color_group_->setExclusive(false);
    checked->setChecked(false);
    color_group_->setExclusive(true);
  }
  ready_button_->setEnabled(true);
  sendState();
}

void robot_gui::setColor(){
  switch (color_group_->checkedId()){
  case 0:
    color_ = "Red";
    setRPose(r_Rpose_);
    break;
  case 1:
    color_ = "Green";
    setRPose(g_Rpose_);
    break;
  case 2:
    color_ = "Blue";
    setRPose(b_Rpose_);
    break;
  default:
    color_ = "No";
    break;
  }
  change_mission_color();
  change_release_pose();
  if(send2camera_)
    sendColor2camera(color_);
}

void robot_gui::removeMission(){
  QItemSelectionModel *selects = script_table_->selectionModel();
  if(selects->hasSelection()){
    QModelIndexList s_list = selects->selectedRows();
    //注意要從row數較後面的開始往前刪除，先山前面的會把後面的往前移
    for(int i=s_list.count()-1;i>=0;i--){
      QModelIndex index = s_list.at(i);
      // qDebug()<<index.row();
      script_->removeRow(index.row());
    }
  }
}

void robot_gui::addMission(){
  QItemSelectionModel *selects = script_table_->selectionModel();
  int row_count = script_->rowCount();
  if(selects->hasSelection()){
    QModelIndexList s_list = selects->selectedRows();
    QModelIndex index = s_list.at(0);
    row_count = index.row();
  }
  QString pose = x_input_->text();
  pose.append(QString(" ,"));
  pose.append(y_input_->text());
  pose.append(QString(" ,"));
  pose.append(theta_input_->text());
  QList<QStandardItem*> insert_data;
  insert_data.append(new QStandardItem(pose));
  insert_data.append(new QStandardItem(action_input_->text()));
  if(color_!="No"&&color_input_->text().toStdString()!=color_
    &&action_input_->text().toStdString()!="Hold"){
    QMessageBox::warning(NULL,"Warning","Color Wrong",QMessageBox::Ok,QMessageBox::Ok);
    return;
  }
  insert_data.append(new QStandardItem(color_input_->text()));
  
  script_->insertRow(row_count,insert_data);
  for (int j=0; j < column_number_; j++){
    script_->item(row_count,j)->setTextAlignment(Qt::AlignCenter);
  }
  
}

void robot_gui::getScript(){
  XmlRpc::XmlRpcValue script;
  nh_local_.param("mission_script",script,script);

  for(int i=0;i<script.size();i++){
    XmlRpc::XmlRpcValue mission = script[i];
    QString pose = QString::number(double(mission[0]));
    pose.append(QString(" ,"));
    pose.append(QString::number(double(mission[1])));
    pose.append(QString(" ,"));
    pose.append(QString::number(double(mission[2])));
    script_->setItem(i,0,new QStandardItem(pose));
    QString a = QString::fromStdString(string(mission[3]));//action
    QString c = QString::fromStdString(string(mission[4]));//color
    script_->setItem(i,1,new QStandardItem(a));
    script_->setItem(i,2,new QStandardItem(c));
    for (int j=0; j < column_number_; j++){
      script_->item(i,j)->setTextAlignment(Qt::AlignCenter);
    }
  }
}

void robot_gui::sendState(){
  std_msgs::String r_state;
  r_state.data = r_state_;
  state_pub.publish(r_state);

  if(r_state_ == "Ready"){
    if(gui_sendScript_){
      std_msgs::Int32 m_count;
      m_count.data = script_->rowCount();
      mCount_pub.publish(m_count);
    }
    else{
      if(color_!="No"){
        std_msgs::String m_color;
        m_color.data = color_;
        color_pub.publish(m_color);
      }
    }
  }
}

void robot_gui::sendColor2camera(string c){
  robot_main::main2arm camera_output;
  camera_output.action = "Grab";
  camera_output.color = c;
  camera_pub.publish(camera_output);
}

bool robot_gui::return_mission(robot_main::getMission::Request &req,robot_main::getMission::Response &res){
  // qDebug() << "Work";
  if(req.m_num >= script_->rowCount()){
    for(int i=0;i<column_number_;i++){
      script_->item(req.m_num-1,i)->setData(QVariant(QBrush(Qt::white)), Qt::BackgroundRole);
    }
    res.action = "End"; //tell main to stop
    return true;
  }

  QString s_total, s_x, s_y, s_theta; // Qstring of x, y, theta
  s_total = script_->item(req.m_num,0)->text();
  s_x = s_total.split(" ,").at(0);
  s_y = s_total.split(" ,").at(1);
  s_theta = s_total.split(" ,").at(2);
  qDebug() << s_total << s_x << s_y << s_theta;
  res.x = s_x.toFloat();
  res.y = s_y.toFloat();
  res.theta = s_theta.toFloat();
  res.action = script_->item(req.m_num,1)->text().toStdString();
  res.color = script_->item(req.m_num,2)->text().toStdString();

  //change ondoing mission color
  if(req.m_num > 0){ //clear last mission color
    for(int i=0;i<column_number_;i++){
      script_->item(req.m_num-1,i)->setData(QVariant(QBrush(Qt::white)), Qt::BackgroundRole);
    }
  }
  for(int i=0;i<column_number_;i++){ //color now mission
    script_->item(req.m_num,i)->setData(QVariant(QBrush(QColor(255, 0, 0, 127))), Qt::BackgroundRole);
  }
  return true;
}

void robot_gui::setRPose(XmlRpc::XmlRpcValue input){
  ReleasePose_.clear();
  ReleasePose_ = QString::number( double(input[0]) );
  ReleasePose_.append( QString(" ,") );
  ReleasePose_.append( QString::number(double(input[1])) );
  ReleasePose_.append( QString(" ,") );
  ReleasePose_.append( QString::number(double(input[2])) );
}

void robot_gui::change_mission_color(){
  int row_count = script_->rowCount();
  for(int i=0; i<row_count; i++){
    if(script_->item(i,1)->text().toStdString()!="Hold"){ //grab and release mission will change color
      script_->setItem(i,2,new QStandardItem(QString::fromStdString(color_)));
      script_->item(i,2)->setTextAlignment(Qt::AlignCenter);
    }
  }
  script_table_->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
  return;
}

void robot_gui::change_release_pose(){
  if(!threeReleaseMission_ )
    return;

  int row_count = script_->rowCount();
  for(int i=0; i<row_count; i++){
    if(script_->item(i,1)->text().toStdString()=="Release"){
      script_->setItem(i,0,new QStandardItem(ReleasePose_));
      script_->item(i,0)->setTextAlignment(Qt::AlignCenter);
    }
  }
  script_table_->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
  return;

}

void robot_gui::save(rviz::Config config) const {
  rviz::Panel::save(config);
}

void robot_gui::load(const rviz::Config& config) {
  rviz::Panel::load(config);
}

#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(robot_main::robot_gui,rviz::Panel)

/*
//Question 
 1. addItem in QT?
 2.
 3.
*/