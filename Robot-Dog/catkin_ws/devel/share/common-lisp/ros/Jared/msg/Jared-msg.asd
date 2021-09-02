
(cl:in-package :asdf)

(defsystem "Jared-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "simpleMoteus" :depends-on ("_package_simpleMoteus"))
    (:file "_package_simpleMoteus" :depends-on ("_package"))
  ))