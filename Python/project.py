import cv2 as cv
import numpy as np
import time
import mediapipe as mp

midline = 140
interval = 30

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
pose_coord = [[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None]]
pose_coord = np.array(pose_coord)
video = cv.VideoCapture(0)
ret, frame = video.read()
frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)
results = pose.process(frame)
y_dist_left = 0
y_dist_avg = 0
y_dist_array = []

if not video.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = video.read()
    frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)   
    results = pose.process(frame)
    mpDraw.draw_landmarks(frame,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
    frame = cv.rectangle(frame,(40,40),(210,110),(0,0,0),thickness=cv.FILLED)
    frame = cv.rectangle(frame,(50,50),(200,100),(200,145,59),thickness=cv.FILLED)
    frame = cv.putText(frame, 'Neck:', (70,90), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)

    if results.pose_landmarks is not None:    
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w,c = frame.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            pose_coord[id] = [cx,cy]

        y_dist_left = pose_coord[11][1] - pose_coord[9][1]    
        if y_dist_left > (midline + interval):
            frame = cv.rectangle(frame,(40,120),(210,350),(0,0,0),thickness=cv.FILLED)
            frame = cv.rectangle(frame,(50,130),(200,340),(230,124,176),thickness=cv.FILLED)
            frame = cv.putText(frame, 'Bend', (70,190), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
            frame = cv.putText(frame, 'a bit', (70,240), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
            frame = cv.putText(frame, 'forward!', (60,290), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)

        elif y_dist_left < (midline - interval):
            frame = cv.rectangle(frame,(40,120),(210,350),(0,0,0),thickness=cv.FILLED)
            frame = cv.rectangle(frame,(50,130),(200,340),(160,210,196),thickness=cv.FILLED)
            frame = cv.putText(frame, 'Bend', (70,190), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
            frame = cv.putText(frame, 'a bit', (70,240), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
            frame = cv.putText(frame, 'back!', (60,290), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)

        else:
            frame = cv.rectangle(frame,(40,120),(210,350),(0,0,0),thickness=cv.FILLED)
            frame = cv.rectangle(frame,(50,130),(200,340),(130,140,245),thickness=cv.FILLED)
            frame = cv.putText(frame, 'You\'re', (70,190), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
            frame = cv.putText(frame, 'Good!', (70,240), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
    
    cv.imshow('IEEE QP Team #8 Project: The Back Hackers', frame)
    c = cv.waitKey(1)
    if c == 27:
        break

video.release()
cv.destroyAllWindows()