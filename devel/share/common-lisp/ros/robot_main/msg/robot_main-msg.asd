
(cl:in-package :asdf)

(defsystem "robot_main-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "arm2main" :depends-on ("_package_arm2main"))
    (:file "_package_arm2main" :depends-on ("_package"))
    (:file "main2arm" :depends-on ("_package_main2arm"))
    (:file "_package_main2arm" :depends-on ("_package"))
  ))