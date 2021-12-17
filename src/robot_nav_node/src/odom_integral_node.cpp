//版本：整合底盤、通訊、導航用

#include  <ros/ros.h>
//tf2必要
#include <tf2_ros/transform_broadcaster.h>
#include "tf2_ros/transform_listener.h"
#include <tf2/LinearMath/Quaternion.h>
#include "tf2/LinearMath/Transform.h"
//不確定用處
#include "tf2/convert.h"
#include "tf2/utils.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
#include "tf2_ros/buffer.h"
#include "tf2_ros/message_filter.h"
#include "message_filters/subscriber.h"
//tf2和odom用到的訊息格式
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/TransformStamped.h>
#include <std_msgs/Int32MultiArray.h>
//IMU
#include "sensor_msgs/Imu.h"
//額外的函式庫
#include <vector>
#include <typeinfo>
#include <stdio.h>

using namespace std;
float current_speed[3] = {0.0,0.0,0.0};
float current_imu[3] = {0.0,0.0,0.0};
/**
 *imu data from stm
 *Ax
 *Ay
 *Gz
 */

//msgs格式  v , omega , x , y , theta
void cmd_callback(const geometry_msgs::Twist &twist_aux){ 
    current_speed[0]=twist_aux.linear.x;
    current_speed[1]=twist_aux.linear.y;
    current_speed[2]=twist_aux.angular.z;
};

void cmd_callback2(const std_msgs::Int32MultiArray::ConstPtr &msg){
    current_speed[0]=msg->data[0]/1000000.;
    current_speed[1]=msg->data[1]/1000000.;
    current_speed[2]=msg->data[2]/1000.;
    current_imu[0]=msg->data[6]/1000000.;
    current_imu[1]=msg->data[7]/1000000.;
    current_imu[2]=msg->data[8]/1000000.;
}

int main(int argc, char** argv){
    ros::init(argc, argv, "odom_integral_node");
    ros::NodeHandle n,nh_lcoal("~");
    // ros::Subscriber cmd_vel_sub = n.subscribe("cmd_vel",100, &cmd_callback) ;
    ros::Subscriber cmd_vel_sub2 = n.subscribe("rxST1",10, &cmd_callback2) ;
    ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
    ros::Publisher imu_pub = n.advertise<sensor_msgs::Imu>("imu", 50);
    static tf2_ros::TransformBroadcaster br;

    //default
    double x ;                 // x 0.689
    double y ;                 // y 2.82
    double th ;              // theta -3.14
    double vx = 0.0;         
    double vy = 0.0;
    double vth = 0.0;          // 角速度
    double dt = 0.0;            // 積分時間

    double ax = 0.0;
    double vx_imu = 0.0;
    double ay = 0.0;
    double vy_imu = 0.0;
    double w = 0.0;
    double delta_vx = 0.0;
    double delta_vy = 0.0;

    string odom_name,base_footprint_name;

    nh_lcoal.param<double>("init_x", x, 1.0);
    nh_lcoal.param<double>("init_y", y, 1.5);
    nh_lcoal.param<double>("init_yaw", th, 0.0);
    nh_lcoal.param<string>("odom_name", odom_name, "odom");
    nh_lcoal.param<string>("base_footprint_name", base_footprint_name, "base_footprint");

    ros::Time current_time, last_time;
    current_time = ros::Time::now();
    last_time = ros::Time::now();
    ros::Rate rate(50);
    while( n.ok() ){
        current_time = ros::Time::now();
        vx = current_speed[0];
        vy = current_speed[1];
        vth = current_speed[2];

        dt = (current_time - last_time).toSec();
        // ROS_INFO("time : %f", dt);
        // ROS_INFO("velocity_x : %f", vx);
        // ROS_INFO("velocity_y : %f", vy);
        // ROS_INFO("velocity_w : %f", vth);
        double delta_x = (vx * cos(th) - vy * sin(th)) * dt;
        double delta_y = (vx * sin(th) + vy * cos(th)) * dt;
        double delta_th = vth * dt;

        x += delta_x;
        y += delta_y;
        th += delta_th;

        // ROS_INFO("now_x     : %f", x);
        // ROS_INFO("now_y     : %f", y);
        // ROS_INFO("now_theta : %f", th);

        geometry_msgs::TransformStamped transformStamped;
        transformStamped.header.stamp = current_time;
        transformStamped.header.frame_id = odom_name;
        transformStamped.child_frame_id = base_footprint_name;
        transformStamped.transform.translation.x = x;
        transformStamped.transform.translation.y = y;
        transformStamped.transform.translation.z = 0.0;
        tf2::Quaternion odom_quat;
        odom_quat.setRPY(0, 0, th);
        transformStamped.transform.rotation.x = odom_quat.x();
        transformStamped.transform.rotation.y = odom_quat.y();
        transformStamped.transform.rotation.z = odom_quat.z();
        transformStamped.transform.rotation.w = odom_quat.w();
        br.sendTransform(transformStamped);

        //publish the odometry message 
        nav_msgs::Odometry odom;
        odom.header.stamp = current_time;
        odom.header.frame_id = odom_name;

        //set the position
        tf2::Quaternion Temporary;
        geometry_msgs::Quaternion odom_quat_pub;
        Temporary.setRPY(0, 0, th);
        tf2::convert( Temporary , odom_quat_pub );
        odom.pose.pose.position.x = x;
        odom.pose.pose.position.y = y;
        odom.pose.pose.position.z = 0.0;
        odom.pose.pose.orientation = odom_quat_pub;

        //set the velocity
        odom.child_frame_id = base_footprint_name;
        odom.twist.twist.linear.x = vx;
        odom.twist.twist.linear.y = vy;
        odom.twist.twist.angular.z = vth;
        odom.twist.covariance = {0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.1, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.15};

        //publish the message
        odom_pub.publish(odom);

//--------------- IMU ---------------------

        ax = current_imu[0];
        ay = current_imu[1];
        w  = current_imu[2];

        if(ax < 0.01)
            ax = 0;
        if(ay < 0.01)
            ay = 0;
        
        // cout << "ax: " << ax << endl;
        // cout << "ay: " << ay << endl;

        sensor_msgs::Imu imu_raw;
		imu_raw.header.stamp = current_time;
		imu_raw.header.frame_id = "imu_link";
		
		imu_raw.orientation.x = 0;
		imu_raw.orientation.y = 0;
		imu_raw.orientation.z = 0;
		imu_raw.orientation.w = 0;
		
		imu_raw.linear_acceleration.x = ax; 
		imu_raw.linear_acceleration.y = ay;
		imu_raw.linear_acceleration.z = 0;
        imu_raw.linear_acceleration_covariance = {0.1, 0  , 0,
                                                  0  , 0.1, 0,  
                                                  0  , 0  , 0};

        delta_vx = ax * dt;
        delta_vy = ay * dt;

        // integral
        vx_imu += delta_vx;
        vy_imu += delta_vy;

        // reset when accel = 0
        // if(ax == 0){
        //     vx_imu = 0;
        //     ROS_INFO("reset vx_imu");
        // }
        // if(ay == 0){
        //     vy_imu = 0;
        //     ROS_INFO("reset vy_imu");
        // }
	    
		imu_raw.angular_velocity.x = vx_imu;
		imu_raw.angular_velocity.y = vy_imu;
		imu_raw.angular_velocity.z = w;
        imu_raw.angular_velocity_covariance = {0.5, 0  , 0,
                                               0  , 0.5, 0,  
                                               0  , 0  , 0.1};

		imu_pub.publish(imu_raw); //imu_raw_pub 節點發布消息至imu_data topic

        //tf2_listener();
        ros::spinOnce();
        last_time = ros::Time::now();
        rate.sleep();
    }
    return 0;
}
