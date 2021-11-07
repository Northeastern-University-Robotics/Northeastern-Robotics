import cv2
from reader import Reader

if __name__ == '__main__':
    reader = Reader()
    while True:
        cv2.imshow("Video", reader.read())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Exiting...")
    cv2.destroyAllWindows()
