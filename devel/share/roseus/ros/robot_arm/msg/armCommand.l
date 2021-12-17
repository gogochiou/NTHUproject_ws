;; Auto-generated. Do not edit!


(when (boundp 'robot_arm::armCommand)
  (if (not (find-package "ROBOT_ARM"))
    (make-package "ROBOT_ARM"))
  (shadow 'armCommand (find-package "ROBOT_ARM")))
(unless (find-package "ROBOT_ARM::ARMCOMMAND")
  (make-package "ROBOT_ARM::ARMCOMMAND"))

(in-package "ROS")
;;//! \htmlinclude armCommand.msg.html


(defclass robot_arm::armCommand
  :super ros::object
  :slots (_action _color ))

(defmethod robot_arm::armCommand
  (:init
   (&key
    ((:action __action) "")
    ((:color __color) "")
    )
   (send-super :init)
   (setq _action (string __action))
   (setq _color (string __color))
   self)
  (:action
   (&optional __action)
   (if __action (setq _action __action)) _action)
  (:color
   (&optional __color)
   (if __color (setq _color __color)) _color)
  (:serialization-length
   ()
   (+
    ;; string _action
    4 (length _action)
    ;; string _color
    4 (length _color)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _action
       (write-long (length _action) s) (princ _action s)
     ;; string _color
       (write-long (length _color) s) (princ _color s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _action
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _action (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _color
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _color (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get robot_arm::armCommand :md5sum-) "1b6b8ada7e9a5f60d947c18cb4bccc20")
(setf (get robot_arm::armCommand :datatype-) "robot_arm/armCommand")
(setf (get robot_arm::armCommand :definition-)
      "string action
string color
")



(provide :robot_arm/armCommand "1b6b8ada7e9a5f60d947c18cb4bccc20")


