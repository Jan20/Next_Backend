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

class Lstm_Model:
    
    ###############
    ## Function ##
    ###############
    def build_model(self):
       
        model = Sequential()
        model.add(LSTM(1, return_sequences=False))
        # model.add(LSTM(100,return_sequences=False))
        model.add(Dense(units=1))
        model.add(Activation("linear"))

        model.compile(loss="mse", optimizer="rmsprop")
        
        return model