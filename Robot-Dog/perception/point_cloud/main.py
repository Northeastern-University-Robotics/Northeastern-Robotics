import json
import os
import tempfile
import platform
from pathlib import Path

import cv2
import depthai
import numpy as np
import open3d as o3d

pipeline = depthai.Pipeline()

#setting up RGB camera
cam_rgb = pipeline.create(depthai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)

#setting up stereo depth camera
monoLeft = pipeline.create(depthai.node.MonoCamera)
monoRight = pipeline.create(depthai.node.MonoCamera)
depth = pipeline.create(depthai.node.StereoDepth)

monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)

# Properties
monoLeft.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_480_P)
monoLeft.setBoardSocket(depthai.CameraBoardSocket.LEFT)
monoRight.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_480_P)
monoRight.setBoardSocket(depthai.CameraBoardSocket.RIGHT)

# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
#depth.setDefaultProfilePreset(depthai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(depthai.MedianFilter.MEDIAN_OFF)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)


#RBG OUT
xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

#DEPTH OUT
xout_depth = pipeline.create(depthai.node.XLinkOut)
xout_depth.setStreamName("disparity")
depth.disparity.link(xout_depth.input)

with depthai.Device(pipeline) as device:
  calibData = device.readCalibration()
  q_rgb = device.getOutputQueue("rgb")
  q_depth = device.getOutputQueue("disparity")
  

  frame = None
  detections = []

  while True:
    in_rgb = q_rgb.tryGet()
    in_depth = q_depth.tryGet()
    
    if in_rgb is not None:
      width = in_rgb.getWidth()
      height = in_rgb.getHeight()
      RGBFrame = in_rgb.getCvFrame()
      RGBFrame = o3d.geometry.Image(RGBFrame.astype(np.uint8))
      intrinsics = calibData.getCameraIntrinsics(depthai.CameraBoardSocket.RGB, depthai.Size2f(width, height))  

    if in_depth is not None:
      width = in_depth.getWidth()
      height = in_depth.getHeight()
      depthFrame = in_depth.getFrame()
      depthFrame = o3d.geometry.Image(depthFrame.astype(np.uint16))
      intrinsics = calibData.getCameraIntrinsics(depthai.CameraBoardSocket.RGB, depthai.Size2f(width, height))  

    if in_depth is not None and in_rgb is not None:
      pinCamIntrinsic = o3d.camera.PinholeCameraIntrinsic(width, height, intrinsics[0][0], intrinsics[1][1], intrinsics[0][2], intrinsics[1][2])
      rgbdImage = o3d.geometry.RGBDImage.create_from_color_and_depth(RGBFrame, depthFrame)
      point_cloud  = o3d.geometry.PointCloud.create_from_rgbd_image(rgbdImage, pinCamIntrinsic)
      print(point_cloud)
    
    o3d.visualization.draw_geometries([point_cloud])
    
    if cv2.waitKey(1) == ord('q'):
      break