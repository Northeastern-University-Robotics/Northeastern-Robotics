import depthai as dai


class Reader:
    """Video reading wrapper around OAK-D using DepthAI API.
    """

    def __init__(self, color=True, camera="rgb", resolution=1080, video_size=(1920, 1080)):
        """Initiate a Reader class.

        Args:
            color (boolean): true for color image else mono. [default: True]
            camera (string): use the rgb, left, or right camera. [default: "rgb]
            resolution (int): resolution to read from the camera. [default: 1080]
            video_size (tuple): video size to read (width, height). [default: (1920, 1080)]
        """
        self._color = color
        self._pipeline = dai.Pipeline()
        if self._color:
            self._cam = self._pipeline.create(dai.node.ColorCamera)
        # do we need to declare output stream?
        self._set_properties(camera, resolution, video_size)

    def _set_properties(self, camera, resolution, video_size):
        """Set the properties of the input stream.

        Args:
            camera (string): use the rgb, left, or right camera.
            resolution (int): resolution to read from the camera.
            video_size (tuple): video size to read (width, height).
        """
        if camera == "rgb":
            self._cam.setBoardSocket(dai.CameraBoardSocket.RGB)
        if resolution == 1080:
            self._cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        # set video size
        self._cam.setVideoSize(video_size)
