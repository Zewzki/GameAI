# Pre Processing

import numpy as np
import cv2
from mss import mss
import ctypes
import keyboard
#from tensorflow import keras
import tensorflow as tf
import keras
from keras.applications.xception import Xception
from keras.models import load_model

keras.backend.clear_session()

user = ctypes.windll.user32

sWidth = user.GetSystemMetrics(0)
sHeight = user.GetSystemMetrics(1)

w = int(sWidth / 2)
h = int(sHeight / 2)

print('Width: %s' % sWidth)
print('Height: %s' % sHeight)

boundingBox = {'top': 0, 'left': 0, 'width': sWidth, 'height': sHeight}
actionButtons = ('up', 'down', 'left', 'right', 'z', 'x', 'v' 'q', 'c', 'left shift')

success = True

#weightsPath = 'xceptionNoTop.h5'
weightsPath = 'xception.h5'

nClasses = 10
pressThresh = .8

backbone = Xception(include_top = True, weights = None, input_tensor = None, input_shape = (w, h, 1), classes = nClasses)
backbone.load_weights(weightsPath)

for i in range(0, len(backbone.layers) - 1):
    backbone.layers[i].trainable = False

#backbone.summary()

cv2.namedWindow('Program View')

sct = mss()

def preProcessInput(org):
    print(org.shape)
    org /= 255.0
    org -= 0.5
    org *= 2.0
    return org
    
while success:

    cap = sct.grab(boundingBox)
    cap = np.array(cap)
    cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    cap = cv2.resize(cap, (w, h))
    cap = np.transpose(cap)

    cap = preProcessInput(cap)
    cap = np.expand_dims(cap, axis = 2)
    
    cap = np.expand_dims(cap, axis = 0)
    
    #predictionList = list(m.predict(cap))
    #print(predictionList)

    cv2.imshow('Program View', cap)
    
    key = cv2.waitKey(1)
    if key == 27:
        success = False

cv2.destroyWindow('Program View')
