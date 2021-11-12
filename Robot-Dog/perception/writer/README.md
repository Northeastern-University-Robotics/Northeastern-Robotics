# Writer for DepthAI and OAK-D
Common wrapper for writer images and video from the OAK-D camera using the DepthAI API to the disk.

## Write Video
```python
import cv2
from reader import Reader
from writer import Writer


if __name__ == '__main__':
    path_of_output = "/Users/adityalohia/Library/Mobile Documents/com~apple~CloudDocs/Work/Robotics/Northeastern-Robotics/Robot-Dog/perception/test.mp4"
    reader = Reader()
    writer = None
    while True:
        if writer is None:
            writer = Writer(path_of_output, reader.get_fps(), reader.get_width(), reader.get_height(), ".mp4")

        frame = reader.read()
        writer.write(frame)
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Exiting...")
    cv2.destroyAllWindows()

```