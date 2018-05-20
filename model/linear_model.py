import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import matplotlib.pyplot as plt
import pandas    

class Linear_Model:
    
    ###############
    ## Function ##
    ###############
    def build_model(self):
        
        model = Sequential()
        model.add(Dense(1, input_dim=1))

        model.compile(optimizer='rmsprop',
            loss='mse',
            metrics=['accuracy'])

        model.summary()


        return model
