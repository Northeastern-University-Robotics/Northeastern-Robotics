;; Auto-generated. Do not edit!


(when (boundp 'Jared::simpleMoteus)
  (if (not (find-package "JARED"))
    (make-package "JARED"))
  (shadow 'simpleMoteus (find-package "JARED")))
(unless (find-package "JARED::SIMPLEMOTEUS")
  (make-package "JARED::SIMPLEMOTEUS"))

(in-package "ROS")
;;//! \htmlinclude simpleMoteus.msg.html


(defclass Jared::simpleMoteus
  :super ros::object
  :slots (_position _velocity _torque ))

(defmethod Jared::simpleMoteus
  (:init
   (&key
    ((:position __position) 0.0)
    ((:velocity __velocity) 0.0)
    ((:torque __torque) 0.0)
    )
   (send-super :init)
   (setq _position (float __position))
   (setq _velocity (float __velocity))
   (setq _torque (float __torque))
   self)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:velocity
   (&optional __velocity)
   (if __velocity (setq _velocity __velocity)) _velocity)
  (:torque
   (&optional __torque)
   (if __torque (setq _torque __torque)) _torque)
  (:serialization-length
   ()
   (+
    ;; float64 _position
    8
    ;; float64 _velocity
    8
    ;; float64 _torque
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _position
       (sys::poke _position (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _velocity
       (sys::poke _velocity (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _torque
       (sys::poke _torque (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _position
     (setq _position (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _velocity
     (setq _velocity (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _torque
     (setq _torque (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get Jared::simpleMoteus :md5sum-) "e433883cdedcd3f2276d926b28334eb4")
(setf (get Jared::simpleMoteus :datatype-) "Jared/simpleMoteus")
(setf (get Jared::simpleMoteus :definition-)
      "float64 position
float64 velocity
float64 torque
")



(provide :Jared/simpleMoteus "e433883cdedcd3f2276d926b28334eb4")


