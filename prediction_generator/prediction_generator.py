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

class Prediction_Generator:
    
    initial_value = None
    final_value = None

    def generate_short_term_predictions(self, model, test_X, lag, lagged_series):
        
        print('--------- Initial Value -----------------')
        print(test_X)
        print('-----------------------------------------')

        self.initial_value = test_X[0][0][0]

        t = numpy.zeros((1,1,1))
        t[0][0][0] = test_X
        short_term_predictions = []
        print('--------------initial Prediction -------------')
        t = model.predict(test_X)
        print(t[0][0])
        print('----------------------------------------------')

        short_term_predictions.append(t[0][0])

        for i in range(1, 50):
            
            temp = numpy.zeros((1,1,1))
            print('-------------- TEMP -----------------')
            print(temp)
            temp[0][0][0] = short_term_predictions[i-1]
            print('-------------- TEMP -----------------')
            print('-------------- TEMP[][][] -----------------')
            print(temp[0][0][0])
            print('-------------- TEMP -----------------')
            d = model.predict(temp)
            short_term_predictions.append(d[0][0])

        print('short_term_predictions length: '+ str(len(short_term_predictions)))
        self.final_value = short_term_predictions[len(short_term_predictions)-1]

        dates = []

        if (len(lagged_series) > 0):
            for i in range(49, -1, -1):
                dates.append(lagged_series['date'][i])

        print('dates length: '+ str(len(dates)))

        if (len(lagged_series) == 0):
            for i in range(1,51):
                dates.append(str(datetime.date.today() + datetime.timedelta(days=i)))

        print('dates length: '+ str(len(dates)))

        print('------------------ FINAL RESULTS -------------------------------')
        print(pandas.DataFrame(data={'date': dates, 'short_term_prediction': short_term_predictions}))
        print('----------------------------------------------------------------')
        return pandas.DataFrame(data={'date': dates, 'short_term_prediction': short_term_predictions})


