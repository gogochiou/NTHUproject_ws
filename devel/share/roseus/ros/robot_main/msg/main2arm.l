;; Auto-generated. Do not edit!


(when (boundp 'robot_main::main2arm)
  (if (not (find-package "ROBOT_MAIN"))
    (make-package "ROBOT_MAIN"))
  (shadow 'main2arm (find-package "ROBOT_MAIN")))
(unless (find-package "ROBOT_MAIN::MAIN2ARM")
  (make-package "ROBOT_MAIN::MAIN2ARM"))

(in-package "ROS")
;;//! \htmlinclude main2arm.msg.html


(defclass robot_main::main2arm
  :super ros::object
  :slots (_action _color ))

(defmethod robot_main::main2arm
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

(setf (get robot_main::main2arm :md5sum-) "1b6b8ada7e9a5f60d947c18cb4bccc20")
(setf (get robot_main::main2arm :datatype-) "robot_main/main2arm")
(setf (get robot_main::main2arm :definition-)
      "string action
string color
")



(provide :robot_main/main2arm "1b6b8ada7e9a5f60d947c18cb4bccc20")


