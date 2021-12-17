
(cl:in-package :asdf)

(defsystem "robot_arm-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "armCommand" :depends-on ("_package_armCommand"))
    (:file "_package_armCommand" :depends-on ("_package"))
    (:file "armState" :depends-on ("_package_armState"))
    (:file "_package_armState" :depends-on ("_package"))
  ))