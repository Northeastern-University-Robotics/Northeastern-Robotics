import depthai as dai


class Encoder:
    """
    Encodes the depth data from the camera for the RTSP stream.
    """

    def __init__(self, color=True, camera="rgb", resolution=1080, video_size=(1920, 1080), fps=30):
        """
        Initialize the encoder.
        Args:
            color : bool
                use color or grayscale. [default: True]
            camera : str
                use the rgb, left, or right camera. [default: "rgb]
            resolution : int
                resolution to read from the camera. [default: 1080]
            video_size : tuple
                video size to read (width, height). [default: (1920, 1080)]
            fps : int
                frames per second. [default: 30]
        """
        self._device = None
        self._color = color
        self._pipeline = dai.Pipeline()
        if self._color:
            self._cam = self._pipeline.createColorCamera()
            self._set_properties(camera, resolution, video_size, fps)

        self._encoder = self._pipeline.createVideoEncoder()
        self._encoder.setDefaultProfilePreset(video_size[0], video_size[1], fps,
                                              dai.VideoEncoderProperties.Profile.H265_MAIN)
        self._link_encoder()
        self._out = self._pipeline.createXLinkOut()
        self._stream = "encoded"
        self._set_output_property()
        self._link()
        self._set_device()

    def _link_encoder(self) -> None:
        """Link the encoder to the input.
        """
        self._cam.video.link(self._encoder.input)

    def _link(self) -> None:
        """Link the encoder to the output.
        """
        self._encoder.bitstream.link(self._out.input)

    def _set_output_property(self) -> None:
        """Set the output property of the reader.
        """
        self._out.setStreamName(self._stream)

    def _set_properties(self, camera, resolution, video_size, fps) -> None:
        """Set the properties of the input stream.

        Args:
            camera : str
                use the rgb, left, or right camera. [default: "rgb]
            resolution : int
                resolution to read from the camera. [default: 1080]
            video_size : tuple
                video size to read (width, height). [default: (1920, 1080)]
            fps : int
                frames per second. [default: 30]
        """
        if resolution == 1080:
            self._cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self._cam.setInterleaved(False)
        self._cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
        self._cam.setFps(fps)

    def _set_device(self) -> None:
        """Set the device to the reader.
        """
        self._device = dai.Device(self._pipeline)

    def __next__(self):
        """
        Get the next frame from the encoder.
        Returns:
            frame : dai.Frame
                the next frame from the encoder.
        """
        return self._device.getOutputQueue(self._stream, maxSize=1, blocking=False)

    def read(self):
        """
        Read the next frame from the encoder.
        Returns:
            frame : encoded frame from the camera.
        """
        return self.__next__().get().getData()
