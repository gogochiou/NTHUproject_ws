; Auto-generated. Do not edit!


(cl:in-package robot_arm-msg)


;//! \htmlinclude armState.msg.html

(cl:defclass <armState> (roslisp-msg-protocol:ros-message)
  ((action
    :reader action
    :initarg :action
    :type cl:string
    :initform "")
   (situation
    :reader situation
    :initarg :situation
    :type cl:string
    :initform ""))
)

(cl:defclass armState (<armState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <armState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'armState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name robot_arm-msg:<armState> is deprecated: use robot_arm-msg:armState instead.")))

(cl:ensure-generic-function 'action-val :lambda-list '(m))
(cl:defmethod action-val ((m <armState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_arm-msg:action-val is deprecated.  Use robot_arm-msg:action instead.")
  (action m))

(cl:ensure-generic-function 'situation-val :lambda-list '(m))
(cl:defmethod situation-val ((m <armState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_arm-msg:situation-val is deprecated.  Use robot_arm-msg:situation instead.")
  (situation m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <armState>) ostream)
  "Serializes a message object of type '<armState>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'action))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'action))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'situation))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'situation))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <armState>) istream)
  "Deserializes a message object of type '<armState>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'action) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'action) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'situation) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'situation) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<armState>)))
  "Returns string type for a message object of type '<armState>"
  "robot_arm/armState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'armState)))
  "Returns string type for a message object of type 'armState"
  "robot_arm/armState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<armState>)))
  "Returns md5sum for a message object of type '<armState>"
  "34e8372aba9fdf90a3e4bf2cfa63f7e3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'armState)))
  "Returns md5sum for a message object of type 'armState"
  "34e8372aba9fdf90a3e4bf2cfa63f7e3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<armState>)))
  "Returns full string definition for message of type '<armState>"
  (cl:format cl:nil "string action~%string situation~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'armState)))
  "Returns full string definition for message of type 'armState"
  (cl:format cl:nil "string action~%string situation~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <armState>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'action))
     4 (cl:length (cl:slot-value msg 'situation))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <armState>))
  "Converts a ROS message object to a list"
  (cl:list 'armState
    (cl:cons ':action (action msg))
    (cl:cons ':situation (situation msg))
))
