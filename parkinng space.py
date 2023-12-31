import cv2
import pickle
width,height=(158-50),(240-192)
try:
    with open('carparkpos','rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []


def mouseClick (event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(poslist):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                poslist.pop(i)
    with open('carparkpos','wb')as f:
        pickle.dump(poslist,f)



while True:
    img = cv2.imread('carParkImg.png')
    cv2.rectangle(img,(50,192),(158,241),(255,0,255),2)
    for pos in poslist:
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
    cv2.imshow('Image',img)
    cv2.setMouseCallback('Image',mouseClick)
    cv2.waitKey(1)
