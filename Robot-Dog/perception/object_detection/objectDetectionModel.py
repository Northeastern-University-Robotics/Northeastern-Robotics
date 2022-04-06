from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np


class ObjectDetection:

    def __init__(self, pipeline=None, labels=None, confidence_threshold=None, weight_path=None):
        """ Initiate ObjectDetection class.
        :param pipeline: Pipeline object
                Accepts a pipeline object constructed during the Reader initialization.
        :param labels: list
                Accepts a list of labels for detection.
        :param confidence_threshold: float
                Accepts a confidence threshold to filter detections.
        :param weight_path: str
                Accepts a file location to the model weights.
        :param nn_path: str
                Accepts a path to a pre-trained neural network model for object detection
        """
        if weight_path is None:
            self._nn_path = str(
                (Path(__file__).parent / Path(
                    '../models/mobilenet-ssd_openvino_2021.4_6shave.blob')).resolve().absolute())
        else:
            self._nn_path = weight_path
        if not Path(self._nn_path).exists():
            raise FileNotFoundError(
                f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

        if labels is None:
            self._label_map = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
                               "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant",
                               "sheep", "sofa", "train", "tvmonitor"]
        else:
            self._label_map = labels

        if pipeline is None:
            self._pipeline = dai.Pipeline()
        else:
            self._pipeline = pipeline
        self._camRgb = self._pipeline.create(dai.node.ColorCamera)
        self._monoRight = self._pipeline.create(dai.node.MonoCamera)
        self._videoEncoder = self._pipeline.create(dai.node.VideoEncoder)
        self._nn = self._pipeline.create(dai.node.MobileNetDetectionNetwork)
        self._manip = self._pipeline.create(dai.node.ImageManip)
        self._set_out_properties()
        self._set_nn(threshold=confidence_threshold)
        self._set_in_properties()
        self._link()

    def detect(self, text_color=None, camera='main') -> list:
        """ object detection
        :param text_color: the color of the text for each label string
        :param camera: represents the camera input,
                'main' -> RGB camera, 'mono' -> side camera
        :return: a list that each element contains a list of x and y(total of 4 values, xmin, xmax, ymin, ymax),
                    and a label that correspond to this object.
        """
        device = dai.Device(self._pipeline)
        queue_size = 8
        qRight = device.getOutputQueue("right", queue_size)
        qManip = device.getOutputQueue("manip", queue_size)
        qDet = device.getOutputQueue("nn", queue_size)
        qRgbEnc = device.getOutputQueue('h265', maxSize=30, blocking=True)
        detection_coors = []
        if text_color is None:
            text_color = (255, 0, 0)
        videoFile = open('video.h265', 'wb')
        cv2.namedWindow("right", cv2.WINDOW_NORMAL)
        cv2.namedWindow("manip", cv2.WINDOW_NORMAL)
        offsetX, croppedFrame = self._convert_from_mono()

        inRight = qRight.tryGet()
        inManip = qManip.tryGet()
        inDet = qDet.tryGet()

        while qRgbEnc.has():
            qRgbEnc.get().getRaw().data.tofile(videoFile)

        detections = []
        if inDet is not None:
            detections = inDet.detections  # should be inDet.detections <------ discussion needed

        if camera.__eq__('main'):
            if inRight is not None:
                frame = inRight.getCvFrame()  # should be getcvframe <------ discussion needed
            else:
                raise Exception("No input from the main camera")
            if frame is not None:
                detections_coor = self._collect_detections_coor(detections)
                detection_coors.append(detections_coor)
                self._box_detections(detections=detections, frame=frame, offset_x=offsetX, text_color=text_color,
                                     camera='main')
        elif camera.__eq__('mono'):
            if inManip is not None:
                frame_manip = inManip.getCvFrame()  # should be getcvframe <------ discussion needed
            else:
                raise Exception("No input from the Mono camera")
            if frame_manip is not None:
                detections_coor = self._collect_detections_coor(detections)
                detection_coors.append(detections_coor)
                self._box_detections(detections=detections, frame=frame_manip, offset_x=offsetX, text_color=text_color)
        else:
            raise Exception("No such type of camera supported.")

        return detection_coors

    def pipeline(self) -> dai.Pipeline:
        return self._pipeline

    def _set_out_properties(self):
        self._videoOut = self._pipeline.create(dai.node.XLinkOut)
        self._xoutRight = self._pipeline.create(dai.node.XLinkOut)
        self._manipOut = self._pipeline.create(dai.node.XLinkOut)
        self._nnOut = self._pipeline.create(dai.node.XLinkOut)
        self._videoOut.setStreamName('h265')
        self._xoutRight.setStreamName("right")
        self._manipOut.setStreamName("manip")
        self._nnOut.setStreamName("nn")

    def _set_nn(self, threshold=None, threads=None, blocking=None, nn_path=None):
        if threshold is None:
            threshold = 0.5
        if threads is None:
            threads = 2
        if blocking is None:
            blocking = False
        if nn_path is None:
            nn_path = self._nn_path
        self._nn.setConfidenceThreshold(threshold)
        self._nn.setBlobPath(nn_path)
        self._nn.setNumInferenceThreads(threads)
        self._nn.input.setBlocking(blocking)

    def _set_in_properties(self):
        self._camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        self._camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self._monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        self._monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
        self._videoEncoder.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H265_MAIN)
        self._manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)
        self._manip.initialConfig.setResize(300, 300)

    def _link(self):
        self._camRgb.video.link(self._videoEncoder.input)
        self._videoEncoder.bitstream.link(self._videoOut.input)
        self._monoRight.out.link(self._manip.inputImage)
        self._manip.out.link(self._nn.input)
        self._monoRight.out.link(self._xoutRight.input)
        self._manip.out.link(self._manipOut.input)
        self._nn.out.link(self._nnOut.input)

    def _convert_from_mono(self):
        offsetX = (self._monoRight.getResolutionWidth() - self._monoRight.getResolutionHeight()) // 2
        croppedFrame = np.zeros((self._monoRight.getResolutionHeight(), self._monoRight.getResolutionHeight()))
        return offsetX, croppedFrame

    # check if all the fields got initialized with a pipeline.
    def __check_pipeline_set_up(self):
        result = (self._camRgb is None) or (self._monoRight is None) or (self._videoEncoder is None) \
                 or (self._nn is None) or (self._manip is None) or (self._videoOut is None) or (self._xoutRight is None) \
                 or (self._manipOut is None) or (self._nnOut is None)
        return result

    # def _init_queue(self, device):  # question here <---------------------
    #     queue_size = 8
    #     qRight = device.getOutputQueue("right", queue_size)
    #     qManip = device.getOutputQueue("manip", queue_size)
    #     qDet = device.getOutputQueue("nn", queue_size)
    #     qRgbEnc = device.getOutputQueue('h265', maxSize=30, blocking=True)
    #     return qRight, qManip, qDet, qRgbEnc

    @staticmethod
    def _frame_norm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def _collect_detections_coor(self, detections):
        result = []
        for detection in detections:
            label = self._label_map[detection.label]
            coor = [detection.xmin, detection.xmax, detection.ymin, detection.ymax]
            total = [coor, label]
            result.append(total)
        return result

    def _box_detections(self, detections, frame, offset_x, text_color, camera=None):
        for detection in detections:
            bbox = self._frame_norm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            if camera.__eq__('main'):
                bbox[::2] += offset_x
            cv2.putText(frame, self._label_map[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX,
                        0.5,
                        text_color)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.5, text_color)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), text_color, 2)