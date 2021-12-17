; Auto-generated. Do not edit!


(cl:in-package robot_main-srv)


;//! \htmlinclude getMission-request.msg.html

(cl:defclass <getMission-request> (roslisp-msg-protocol:ros-message)
  ((m_num
    :reader m_num
    :initarg :m_num
    :type cl:integer
    :initform 0))
)

(cl:defclass getMission-request (<getMission-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <getMission-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'getMission-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name robot_main-srv:<getMission-request> is deprecated: use robot_main-srv:getMission-request instead.")))

(cl:ensure-generic-function 'm_num-val :lambda-list '(m))
(cl:defmethod m_num-val ((m <getMission-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-srv:m_num-val is deprecated.  Use robot_main-srv:m_num instead.")
  (m_num m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <getMission-request>) ostream)
  "Serializes a message object of type '<getMission-request>"
  (cl:let* ((signed (cl:slot-value msg 'm_num)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <getMission-request>) istream)
  "Deserializes a message object of type '<getMission-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'm_num) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<getMission-request>)))
  "Returns string type for a service object of type '<getMission-request>"
  "robot_main/getMissionRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'getMission-request)))
  "Returns string type for a service object of type 'getMission-request"
  "robot_main/getMissionRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<getMission-request>)))
  "Returns md5sum for a message object of type '<getMission-request>"
  "7992715a17ff2dfb6242bdc6efba1bfe")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'getMission-request)))
  "Returns md5sum for a message object of type 'getMission-request"
  "7992715a17ff2dfb6242bdc6efba1bfe")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<getMission-request>)))
  "Returns full string definition for message of type '<getMission-request>"
  (cl:format cl:nil "int32 m_num~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'getMission-request)))
  "Returns full string definition for message of type 'getMission-request"
  (cl:format cl:nil "int32 m_num~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <getMission-request>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <getMission-request>))
  "Converts a ROS message object to a list"
  (cl:list 'getMission-request
    (cl:cons ':m_num (m_num msg))
))
;//! \htmlinclude getMission-response.msg.html

(cl:defclass <getMission-response> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0)
   (theta
    :reader theta
    :initarg :theta
    :type cl:float
    :initform 0.0)
   (action
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

(cl:defclass getMission-response (<getMission-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <getMission-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'getMission-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name robot_main-srv:<getMission-response> is deprecated: use robot_main-srv:getMission-response instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <getMission-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-srv:x-val is deprecated.  Use robot_main-srv:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <getMission-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-srv:y-val is deprecated.  Use robot_main-srv:y instead.")
  (y m))

(cl:ensure-generic-function 'theta-val :lambda-list '(m))
(cl:defmethod theta-val ((m <getMission-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-srv:theta-val is deprecated.  Use robot_main-srv:theta instead.")
  (theta m))

(cl:ensure-generic-function 'action-val :lambda-list '(m))
(cl:defmethod action-val ((m <getMission-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-srv:action-val is deprecated.  Use robot_main-srv:action instead.")
  (action m))

(cl:ensure-generic-function 'color-val :lambda-list '(m))
(cl:defmethod color-val ((m <getMission-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot_main-srv:color-val is deprecated.  Use robot_main-srv:color instead.")
  (color m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <getMission-response>) ostream)
  "Serializes a message object of type '<getMission-response>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'theta))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <getMission-response>) istream)
  "Deserializes a message object of type '<getMission-response>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'theta) (roslisp-utils:decode-single-float-bits bits)))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<getMission-response>)))
  "Returns string type for a service object of type '<getMission-response>"
  "robot_main/getMissionResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'getMission-response)))
  "Returns string type for a service object of type 'getMission-response"
  "robot_main/getMissionResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<getMission-response>)))
  "Returns md5sum for a message object of type '<getMission-response>"
  "7992715a17ff2dfb6242bdc6efba1bfe")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'getMission-response)))
  "Returns md5sum for a message object of type 'getMission-response"
  "7992715a17ff2dfb6242bdc6efba1bfe")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<getMission-response>)))
  "Returns full string definition for message of type '<getMission-response>"
  (cl:format cl:nil "float32 x~%float32 y~%float32 theta~%string action~%string color~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'getMission-response)))
  "Returns full string definition for message of type 'getMission-response"
  (cl:format cl:nil "float32 x~%float32 y~%float32 theta~%string action~%string color~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <getMission-response>))
  (cl:+ 0
     4
     4
     4
     4 (cl:length (cl:slot-value msg 'action))
     4 (cl:length (cl:slot-value msg 'color))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <getMission-response>))
  "Converts a ROS message object to a list"
  (cl:list 'getMission-response
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':theta (theta msg))
    (cl:cons ':action (action msg))
    (cl:cons ':color (color msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'getMission)))
  'getMission-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'getMission)))
  'getMission-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'getMission)))
  "Returns string type for a service object of type '<getMission>"
  "robot_main/getMission")