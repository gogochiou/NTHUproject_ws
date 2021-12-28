# Robotic with SCARA and Omni-wheel

>**Contributor : [guanlunLu](https://github.com/guanlunlu), [Frank-Jhang](https://github.com/Frank-Jhang), [gogoChiou](https://github.com/gogochiou), [LouisQAQ](https://github.com/Louis208908)**

&emsp;&emsp;此 **project** 是我們四人在 **NTHU PME** 的畢業專題研究題目，主旨在實現一套完整且高效率的移動機器人系統。在實作上，採用3WD Omni萬向輪底盤，上方搭載五連桿式的雙臂SCARA機械手臂，並使用STM32做為控制晶片，搭配ROS架構進行定位導航及視覺辨識的開發與驗證。

---

## :grinning:基本使用

* **Nano** ( 機器人搭載的微電腦 )
    * 開啟 **Lidar 、 Realsense 、 通訊 、 其他子程式**

        ```
        roslaunch robot_main nano.launch
        ```

* 本機電腦
    * 開啟 **main** 、 **rviz & gui** 

        ```
        roslaunch robot_main robot_main.launch
        ```
    
    * 開啟導航 **node**

        ```
        roslaunch robot_nav_node robot_nav.launch
        ```
    
    * 開啟手臂 **node**

        ```
        roslaunch robot_arm robot_arm.launch
        ```

