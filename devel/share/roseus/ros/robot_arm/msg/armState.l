;; Auto-generated. Do not edit!


(when (boundp 'robot_arm::armState)
  (if (not (find-package "ROBOT_ARM"))
    (make-package "ROBOT_ARM"))
  (shadow 'armState (find-package "ROBOT_ARM")))
(unless (find-package "ROBOT_ARM::ARMSTATE")
  (make-package "ROBOT_ARM::ARMSTATE"))

(in-package "ROS")
;;//! \htmlinclude armState.msg.html


(defclass robot_arm::armState
  :super ros::object
  :slots (_action _situation ))

(defmethod robot_arm::armState
  (:init
   (&key
    ((:action __action) "")
    ((:situation __situation) "")
    )
   (send-super :init)
   (setq _action (string __action))
   (setq _situation (string __situation))
   self)
  (:action
   (&optional __action)
   (if __action (setq _action __action)) _action)
  (:situation
   (&optional __situation)
   (if __situation (setq _situation __situation)) _situation)
  (:serialization-length
   ()
   (+
    ;; string _action
    4 (length _action)
    ;; string _situation
    4 (length _situation)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _action
       (write-long (length _action) s) (princ _action s)
     ;; string _situation
       (write-long (length _situation) s) (princ _situation s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _action
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _action (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _situation
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _situation (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get robot_arm::armState :md5sum-) "34e8372aba9fdf90a3e4bf2cfa63f7e3")
(setf (get robot_arm::armState :datatype-) "robot_arm/armState")
(setf (get robot_arm::armState :definition-)
      "string action
string situation
")



(provide :robot_arm/armState "34e8372aba9fdf90a3e4bf2cfa63f7e3")


