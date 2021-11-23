import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from ECE16Lib.Pose import Pose

if __name__ == "__main__":
    pose = Pose()

    while True:
        pose.record()
        pose.process()
        pose.draw()
        pose.coordinates()
        pose.show()
        c = cv.waitKey(1)
        if c == 27:
            break

    pose.release()
    cv.destroyAllWindows()