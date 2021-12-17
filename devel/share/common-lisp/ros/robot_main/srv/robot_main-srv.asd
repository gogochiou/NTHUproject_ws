
(cl:in-package :asdf)

(defsystem "robot_main-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "getMission" :depends-on ("_package_getMission"))
    (:file "_package_getMission" :depends-on ("_package"))
  ))