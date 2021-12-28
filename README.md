# Robotic with SCARA and Omni-wheel

>**Contributor : [guanlunLu](https://github.com/guanlunlu), [Frank-Jhang](https://github.com/Frank-Jhang), [gogoChiou](https://github.com/gogochiou), [LouisQAQ](https://github.com/Louis208908)**

&emsp;&emsp;此 **project** 是我們四人在 **NTHU PME** 的畢業專題研究題目，主旨在實現一套完整且高效率的移動機器人系統。在實作上，採用3WD Omni萬向輪底盤，上方搭載五連桿式的雙臂SCARA機械手臂，並使用STM32做為控制晶片，搭配ROS架構進行定位導航及視覺辨識的開發與驗證。

---

## 基本使用

* **Nano** ( 機器人搭載的微電腦 )
    * 開啟 **Lidar 、 Realsense 、 通訊 、 其他子程式**

        ```
        roslaunch robot_main nano.launch
        ```

* 本機電腦 (個人配置 **Master** 於本機電腦)
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

## **Package** 概略介紹

* 主程式與GUI

    > :heavy_check_mark: **[robot_main](https://github.com/gogochiou/NTHUproject_ws/tree/main/src/robot_main)** <br>
    > :x: **[robot_gui](https://github.com/gogochiou/NTHUproject_ws/tree/main/src/robot_gui)**

    * robot_main

        `&emsp;&emsp;作為 **agent** 管理 **navigation** 以及 **arm** 這兩個系統運行的工作。負責告知後兩者執行的任務，並藉由回傳的資訊得知運作情形。`
        
        此部分包含三個重要程式 :

        1. rviz_panel plugin (gui)
            
            > 使用 **QT** 函式庫，因為 **rviz** 也是建基於 **QT** 的，我們可以使用 **plugin** 的方式，將自定義的介面( 或 **gui** )放入 **rviz** 中。
            
            圖形化介面可幫助我們知道程式運行的資訊，並且也可以操作介面上的按鍵，幫助我們快速地發布指令給程式。

        2. main node

            主要管理 **navigation** 和 **arm** 的程式。

        3. invoke_camera

            此節點作用為在機器人運行到特定情形時，喚醒pcl.launch，開啟顏色辨識的節點。因pcl節點放置於Nano上，所以invoke_camera也必須運行於Nano上(較簡單處理)。


