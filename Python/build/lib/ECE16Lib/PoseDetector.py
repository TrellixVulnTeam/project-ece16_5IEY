import cv2 as cv
from ECE16Lib import pose
from ECE16Lib import drawing_utils
import numpy as np

class Pose:

    def __init__(self):
        self.mpDraw = drawing_utils
        self.mpPose = pose
        self.pose = self.mpPose.Pose()
        self.pose_coord = [[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None]]
        self.pose_coord = np.array(self.pose_coord)
        self.video = cv.VideoCapture(0)
        self.ret, self.frame = self.video.read()
        self.frame = cv.resize(self.frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)
        self.results = self.pose.process(self.frame)
        self.check_opened()
    
    def check_opened(self):
        if not self.video.isOpened():
            raise IOError("Cannot open webcam")

    def record(self):
        self.ret, self.frame = self.video.read()
        self.frame = cv.resize(self.frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)

    def process(self):
        self.results = self.pose.process(self.frame)

    def draw(self):
        self.mpDraw.draw_landmarks(self.frame,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)

    def coordinates(self):
        if self.results.pose_landmarks is not None:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w,c = self.frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.pose_coord[id] = [cx,cy]

    def show(self):
        cv.imshow('TwistAR', self.frame)

    def release(self):
        self.video.release()