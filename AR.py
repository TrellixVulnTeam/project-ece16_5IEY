import cv2
import numpy as np

cap = cv2.VideoCapture(0)
imgTarget = cv2.imread('/Users/gk/Desktop/E16Project/project-ece16/mat.jpg')
imgVideo = cv2.imread('/Users/gk/Desktop/E16Project/project-ece16/board.png')
h,w,c = imgTarget.shape
imgVideo = cv2.resize(imgVideo,(w,h))

orb = cv2.ORB_create(nfeatures=10000)
k1, d1 = orb.detectAndCompute(imgTarget,None)
# imgTarget = cv2.drawKeypoints(imgTarget,k1,None)

while True:
    ret, frame = cap.read()
    imgAug = frame.copy()
    k2, d2 = orb.detectAndCompute(frame,None)
    # frame = cv2.drawKeypoints(frame,k2,None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(d1,d2,k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    print(len(good))

    imgFeatures = cv2.drawMatches(imgTarget,k1,frame,k2,good,None,flags=2)
    if len(good) > 5:
        src = np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst = np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        matrix, mask = cv2.findHomography(src,dst,cv2.RANSAC,5)
        print(matrix)

        pts = np.float32([[0,0],[0,h],[w,h],[w,0]]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,matrix)
        img2 = cv2.polylines(frame,[np.int32(dst)],True,(255,0,255),3)
        imgWarp = cv2.warpPerspective(imgVideo,matrix,(frame.shape[1],frame.shape[0]))

        maskNew = np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
        cv2.fillPoly(maskNew,[np.int32(dst)],(255,255,255))
        maskInv = cv2.bitwise_not(maskNew)
        imgAug = cv2.bitwise_and(imgAug,imgAug,mask = maskInv)
        imgAug = cv2.bitwise_or(imgWarp,imgAug)


        #cv2.imshow('imgAug',imgAug)
        #cv2.imshow('maskInv',maskInv)
        #cv2.imshow('maskNew',maskNew)
        #cv2.imshow('ImgWarp',imgWarp)
        #cv2.imshow('Img2',img2)
    
    #cv2.imshow('ImgFeatures',imgFeatures)
    #cv2.imshow('ImgTarget',imgTarget)
    #cv2.imshow('myVid',imgVideo)
    #cv2.imshow('Webcam',frame)
    c = cv2.waitKey(1)
    if c == 27:
        break


cv2.destroyAllWindows()
