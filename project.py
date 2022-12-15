import cv2
import mediapipe as mp
import math
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands 
hands = mpHands.Hands()


cap = cv2.VideoCapture(0)
while True:
    success,img = cap.read()
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList =[]
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x*w) , int(lm.y*h)
                lmList.append([id,cx,cy])
                # print(lmList)
            # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            
            if lmList:
                x1,y1 = lmList[4][1], lmList[4][2]
                x2,y2 = lmList[8][1], lmList[8][2]
                cv2.circle(img, (x1,y1), 15, (134,45,45), cv2.FILLED)
                cv2.circle(img, (x2,y2), 15, (134,45,45), cv2.FILLED)
                cv2.line(img, (x1,y1), (x2,y2), (134,45,45), 3)
                length = math.hypot(x2-x1, y2-y1)
                # print(length)
                vol = np.interp(length, [50 ,300],[minVol, maxVol])
                volBar = np.interp(length , [50 ,300] , [400 ,150])
                volPer = np.interp(length , [50 ,300] , [0 ,100])
                volume.SetMasterVolumeLevel(vol, None)
                cv2.rectangle(img , (50 ,150) , (85 , 400) ,(123,213,122) ,3)
                cv2.rectangle(img , (50 , int(volBar)) , (85 ,400) ,(0, 231,23) ,cv2.FILLED)
                cv2.putText(img , str(int(volPer)) , (40, 450) ,cv2.FONT_HERSHEY_PLAIN ,4 , (24,34,34) , 3)
                
                
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
