; Auto-generated. Do not edit!


(cl:in-package robot_main-msg)


;//! \htmlinclude main2arm.msg.html

(cl:defclass <main2arm> (roslisp-msg-protocol:ros-message)
  ((action
    :reader action
    :initarg :action
    :type cl:string
    :initform "")
   (color
    :reader color
    :initarg :color
    :type cl:string
    :initform ""))
)

(cl:defclass main2arm (<main2arm>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <main2arm>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'main2arm)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name robot_main-msg:<main2arm> is deprecated: use robot_main-msg:main2arm instead.")))

(cl:ensure-generic-function 'action-val :lambda-list '(m))
(cl:defmethod action-val ((m <main2arm>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-msg:action-val is deprecated.  Use robot_main-msg:action instead.")
  (action m))

(cl:ensure-generic-function 'color-val :lambda-list '(m))
(cl:defmethod color-val ((m <main2arm>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-msg:color-val is deprecated.  Use robot_main-msg:color instead.")
  (color m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <main2arm>) ostream)
  "Serializes a message object of type '<main2arm>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'action))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'action))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'color))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'color))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <main2arm>) istream)
  "Deserializes a message object of type '<main2arm>"
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
      (cl:setf (cl:slot-value msg 'color) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'color) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<main2arm>)))
  "Returns string type for a message object of type '<main2arm>"
  "robot_main/main2arm")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'main2arm)))
  "Returns string type for a message object of type 'main2arm"
  "robot_main/main2arm")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<main2arm>)))
  "Returns md5sum for a message object of type '<main2arm>"
  "1b6b8ada7e9a5f60d947c18cb4bccc20")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'main2arm)))
  "Returns md5sum for a message object of type 'main2arm"
  "1b6b8ada7e9a5f60d947c18cb4bccc20")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<main2arm>)))
  "Returns full string definition for message of type '<main2arm>"
  (cl:format cl:nil "string action~%string color~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'main2arm)))
  "Returns full string definition for message of type 'main2arm"
  (cl:format cl:nil "string action~%string color~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <main2arm>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'action))
     4 (cl:length (cl:slot-value msg 'color))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <main2arm>))
  "Converts a ROS message object to a list"
  (cl:list 'main2arm
    (cl:cons ':action (action msg))
    (cl:cons ':color (color msg))
))
