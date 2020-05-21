import numpy as np
import cv2
from mss import mss
import ctypes

user = ctypes.windll.user32

sWidth = user.GetSystemMetrics(0)
sHeight = user.GetSystemMetrics(1)

boundingBox = {'top': 0, 'left': 0, 'width': sWidth, 'height': sHeight}

cv2.namedWindow('test')

sct = mss()

success = True

while success:

    cap = sct.grab(boundingBox)
    cap = np.array(cap)

    r = cap[:, :, 0]
    g = cap[:, :, 1]
    b = cap[:, :, 2]

    r = cv2.Canny(r, 100, 200)
    g = cv2.Canny(g, 100, 200)
    b = cv2.Canny(b, 100, 200)

    cap[:, :, 0] = r
    cap[:, :, 1] = g
    cap[:, :, 2] = b

    #cap = cv2.resize(cap, (int(sWidth / 2), int(sHeight / 2)))
    
    cv2.imshow('test', cap)

    key = cv2.waitKey(1)
    if key == 27:
        success = False

cv2.destroyWindow('test')
