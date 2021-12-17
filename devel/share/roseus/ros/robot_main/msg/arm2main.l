;; Auto-generated. Do not edit!


(when (boundp 'robot_main::arm2main)
  (if (not (find-package "ROBOT_MAIN"))
    (make-package "ROBOT_MAIN"))
  (shadow 'arm2main (find-package "ROBOT_MAIN")))
(unless (find-package "ROBOT_MAIN::ARM2MAIN")
  (make-package "ROBOT_MAIN::ARM2MAIN"))

(in-package "ROS")
;;//! \htmlinclude arm2main.msg.html


(defclass robot_main::arm2main
  :super ros::object
  :slots (_action _situation ))

(defmethod robot_main::arm2main
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

(setf (get robot_main::arm2main :md5sum-) "34e8372aba9fdf90a3e4bf2cfa63f7e3")
(setf (get robot_main::arm2main :datatype-) "robot_main/arm2main")
(setf (get robot_main::arm2main :definition-)
      "string action
string situation
")



(provide :robot_main/arm2main "34e8372aba9fdf90a3e4bf2cfa63f7e3")


