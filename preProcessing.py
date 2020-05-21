# Pre Processing

import numpy as np
import cv2
from mss import mss
import ctypes
import keyboard
#from tensorflow import keras
import tensorflow as tf
import keras

user = ctypes.windll.user32

sWidth = user.GetSystemMetrics(0)
sHeight = user.GetSystemMetrics(1)

w = int(sWidth / 2)
h = int(sHeight / 2)

print('Width: %s' % sWidth)
print('Height: %s' % sHeight)

boundingBox = {'top': 0, 'left': 0, 'width': sWidth, 'height': sHeight}
actionButtons = ('up', 'down', 'left', 'right', 'z', 'x', 'v' 'q', 'c', 'left shift')

cv2.namedWindow('Program View')

sct = mss()

success = True

def createModel():

    model = keras.Sequential()

    model.add(keras.layers.Conv2D(32, (3, 3), padding = 'same', activation = 'relu', input_shape = (h, w, 3)))
    model.add(keras.layers.Conv2D(32, (3, 3), padding = 'same', activation = 'relu'))
    model.add(keras.layers.MaxPool2D())

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(512, activation = 'relu'))
    model.add(keras.layers.Dense(128, activation = 'relu'))
    model.add(keras.layers.Dense(10, activation = 'relu'))

    return model

adam = keras.optimizers.Adam(learning_rate = .00001)
m = createModel()
m.compile(optimizer = adam, loss = 'categorical_crossentropy', metrics = ['accuracy'])
    
while success:

    cap = sct.grab(boundingBox)
    cap = np.array(cap)

    cap = cv2.resize(cap, (w, h))
    cv2.imshow('Program View', cap)

    dimmedCap = cap[:, :, 0:3]
    dimmedCap = np.expand_dims(np.array(dimmedCap), axis = 0)
    
    #predictionList = list(m.predict(dimmedCap))
    #print(predictionList)

    key = cv2.waitKey(1)
    if key == 27:
        success = False

cv2.destroyWindow('Program View')
