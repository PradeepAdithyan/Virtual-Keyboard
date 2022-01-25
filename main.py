import cv2
import numpy as np
import mediapipe as mp
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap=cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)

mphands = mp.solutions.hands
hands= mphands.Hands(False,2,0.7,0.5)

mpDraw= mp.solutions.drawing_utils

while True:
    res, img= cap.read()
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result= hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for i in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, i,mphands.HAND_CONNECTIONS)

    xList = []
    yList = []
    bbox = []
    lmList = []
    if result.multi_hand_landmarks:
        myHand = result.multi_hand_landmarks[0]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            xList.append(cx)
            yList.append(cy)
            lmList.append([id, cx, cy])
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        xmin, xmax = min(xList), max(xList)
        ymin, ymax = min(yList),max(yList)
        bbox = xmin, ymin, xmax, ymax

        cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                  (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)


        fingers = []
        tipIds=[4,8,12,16,20]
        if lmList[tipIds[0]][1] >lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] <lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        x1,y1=lmList[tipIds[0]][1],lmList[tipIds[0]][2]
        x2,y2=lmList[tipIds[1]][1],lmList[tipIds[1]][2]
        cen_x,cen_y= (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),5,(0,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2), (0, 255, 255),3)
        cv2.circle(img, (cen_x, cen_y), 15, (0, 0, 255), cv2.FILLED)
        length= math.hypot(x2-x1,y2-y1)

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        vol=np.interp(length,[50,300],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol,None)

    cv2.imshow("HAND DETECTOR",img)
    cv2.waitKey(1)