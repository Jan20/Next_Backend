import pandas
from pandas import DataFrame
import keras.backend.tensorflow_backend
import numpy as numpy
import matplotlib.pyplot as plt
import math
import datetime
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation, Dropout
from keras import backend as K
from sklearn.metrics import mean_squared_error
from database.database import Database
from data_import.data_import import Data_Import
from prediction.prediction import Prediction
import time 

class Model:
    
    ###############
    ## Function ##
    ###############
    def build_model(self):
        
        # model = Sequential()
        # model.add(LSTM(input_shape=(50, 1), units=1, return_sequences=False))
        # # model.add(LSTM(100,return_sequences=False))
        # model.add(Dense(units=1))
        # model.add(Activation("linear"))

        # start = time.time()
        # model.compile(loss="mse", optimizer="rmsprop")
        # print("> Compilation Time : ", time.time() - start)
        
        # return model


        # create model
        model = Sequential()
        model.add(Dense(13, input_dim=13, kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        # Compile model
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model