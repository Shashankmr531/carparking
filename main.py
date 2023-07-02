import cv2
import cvzone
import numpy as np
import pickle
width,height=(158-50),(240-192)
cap = cv2.VideoCapture('carPark.mp4')
try:
    with open('carparkpos','rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []
def Checkparkspace(imgpro):
    spacecounter=0
    for pos in poslist:
        x,y=pos
       # cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        cv2.imshow('video',img)
        imgcrop = imgpro[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgcrop)
        count=cv2.countNonZero(imgcrop)
        cvzone.putTextRect(img,str(count),(x,y+height-2),scale=1,thickness=1,offset=0,colorR=(0,0,255))
        if count<500:
            color=(0,255,0)
            thickness=2
            spacecounter+=1;
        else:
            color=(0,0,255)
            thickness=2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color, thickness)
    cvzone.putTextRect(img,f'FREE{str(spacecounter)}/{len(poslist)}',(400,80),scale=2,thickness=3,offset=0,colorR=(0,255,0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgblur=cv2.GaussianBlur(imgGray,(3,3),1)
    imgthreshold=cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV,25,16)
    imgmedian=cv2.medianBlur(imgthreshold,5)
    kernel=np.zeros((3,3),np.uint8)
    imgdilate=cv2.dilate(imgmedian,kernel,iterations=1)

    Checkparkspace(imgdilate)
    for pos in poslist:
        x,y=pos
        # cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    cv2.imshow('video', img)
    # cv2.imshow('imgblur', imgblur)
    # cv2.imshow('thresh', imgthreshold)
    # cv2.imshow('thresh1',imgmedian)
    # cv2.imshow('thresh2',imgdilate)
    cv2.waitKey(1)
