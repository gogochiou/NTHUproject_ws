;; Auto-generated. Do not edit!


(when (boundp 'robot_main::getMission)
  (if (not (find-package "ROBOT_MAIN"))
    (make-package "ROBOT_MAIN"))
  (shadow 'getMission (find-package "ROBOT_MAIN")))
(unless (find-package "ROBOT_MAIN::GETMISSION")
  (make-package "ROBOT_MAIN::GETMISSION"))
(unless (find-package "ROBOT_MAIN::GETMISSIONREQUEST")
  (make-package "ROBOT_MAIN::GETMISSIONREQUEST"))
(unless (find-package "ROBOT_MAIN::GETMISSIONRESPONSE")
  (make-package "ROBOT_MAIN::GETMISSIONRESPONSE"))

(in-package "ROS")





(defclass robot_main::getMissionRequest
  :super ros::object
  :slots (_m_num ))

(defmethod robot_main::getMissionRequest
  (:init
   (&key
    ((:m_num __m_num) 0)
    )
   (send-super :init)
   (setq _m_num (round __m_num))
   self)
  (:m_num
   (&optional __m_num)
   (if __m_num (setq _m_num __m_num)) _m_num)
  (:serialization-length
   ()
   (+
    ;; int32 _m_num
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _m_num
       (write-long _m_num s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _m_num
     (setq _m_num (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass robot_main::getMissionResponse
  :super ros::object
  :slots (_x _y _theta _action _color ))

(defmethod robot_main::getMissionResponse
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:theta __theta) 0.0)
    ((:action __action) "")
    ((:color __color) "")
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _theta (float __theta))
   (setq _action (string __action))
   (setq _color (string __color))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:theta
   (&optional __theta)
   (if __theta (setq _theta __theta)) _theta)
  (:action
   (&optional __action)
   (if __action (setq _action __action)) _action)
  (:color
   (&optional __color)
   (if __color (setq _color __color)) _color)
  (:serialization-length
   ()
   (+
    ;; float32 _x
    4
    ;; float32 _y
    4
    ;; float32 _theta
    4
    ;; string _action
    4 (length _action)
    ;; string _color
    4 (length _color)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _x
       (sys::poke _x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y
       (sys::poke _y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _theta
       (sys::poke _theta (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; string _action
       (write-long (length _action) s) (princ _action s)
     ;; string _color
       (write-long (length _color) s) (princ _color s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _x
     (setq _x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y
     (setq _y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _theta
     (setq _theta (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; string _action
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _action (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _color
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _color (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass robot_main::getMission
  :super ros::object
  :slots ())

(setf (get robot_main::getMission :md5sum-) "7992715a17ff2dfb6242bdc6efba1bfe")
(setf (get robot_main::getMission :datatype-) "robot_main/getMission")
(setf (get robot_main::getMission :request) robot_main::getMissionRequest)
(setf (get robot_main::getMission :response) robot_main::getMissionResponse)

(defmethod robot_main::getMissionRequest
  (:response () (instance robot_main::getMissionResponse :init)))

(setf (get robot_main::getMissionRequest :md5sum-) "7992715a17ff2dfb6242bdc6efba1bfe")
(setf (get robot_main::getMissionRequest :datatype-) "robot_main/getMissionRequest")
(setf (get robot_main::getMissionRequest :definition-)
      "int32 m_num
---
float32 x
float32 y
float32 theta
string action
string color
")

(setf (get robot_main::getMissionResponse :md5sum-) "7992715a17ff2dfb6242bdc6efba1bfe")
(setf (get robot_main::getMissionResponse :datatype-) "robot_main/getMissionResponse")
(setf (get robot_main::getMissionResponse :definition-)
      "int32 m_num
---
float32 x
float32 y
float32 theta
string action
string color
")



(provide :robot_main/getMission "7992715a17ff2dfb6242bdc6efba1bfe")


