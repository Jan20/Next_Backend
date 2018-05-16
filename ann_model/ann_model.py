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
from pipeline.pipeline import Pipeline
from prediction_generator.prediction_generator import Prediction_Generator

class ANN_Model:
    
    def __init__(self):

        print('Hello')
    
    ###############
    ## Variables ##
    ###############
    epochs = 10
    batch_size = 1
    db = Database()

    initial_value = None
    final_value = None

    def execute(self, series, lag):

        pipeline = Pipeline()
        prediction_generator = Prediction_Generator()

        reduced_series = pipeline.reduce_series(series, lag)
        lagged_series = pipeline.get_lagged_series(series, lag)
        normalized_series = pipeline.normalize_data(reduced_series)
        supervised_series = pipeline.series_to_supervised(normalized_series, 1, 1, True)
        train_X, train_y, test_X, test_y = pipeline.create_train_and_test_sets(supervised_series)
        ann_model = self.create_core_model(train_X, train_y, test_X, test_y)
        print('----------------- INPUTS ------------------')
        print(len(lagged_series))
        print('---------------- /INPUTS ------------------')
        normalized_short_term_predictions = prediction_generator.generate_short_term_predictions(ann_model, test_X, lag, lagged_series)
        
        # Ugly
        self.initial_value = prediction_generator.initial_value
        self.final_value = prediction_generator.final_value
        
        return pipeline.inverse_predictions(normalized_short_term_predictions)


    def create_core_model(self, train_X, train_y, test_X, test_y):
        
        if keras.backend.tensorflow_backend._SESSION:
            tf.reset_default_graph() 
            keras.backend.tensorflow_backend._SESSION.close()
            keras.backend.tensorflow_backend._SESSION = None
        
        K.clear_session()
        model = None
        print('Keras ANN')
        print(train_X.shape[1])
        print(train_X.shape[2])
        print('---------------- Nice _-----------------------')
        print(train_X)
        # model = Sequential()
        # model.add(Dense(12, input_shape=(train_X.shape[0][0][0], train_X.shape[1]), activation='relu'))
        # model.add(Dense(8, activation='relu'))
        # model.add(Dense(1, activation='sigmoid'))

        # ---------------------------------

        # model.add(LSTM(100, input_shape=(train_X.shape[1], train_X.shape[2]), batch_size=self.batch_size, return_sequences=True))
        # model.add(LSTM(100, return_sequences=False, batch_size=self.batch_size))
        # model.add(Dense(1))

        
        # model.add(LSTM(12, input_shape=(train_X.shape[1], train_X.shape[2])))
        # model.add(Dropout(0.2))
        # model.add(Dense(1))






        model = Sequential()

        model.add(LSTM(
            input_dim=train_X.shape[0],
            output_dim=train_X.shape[1],
            return_sequences=True))
        model.add(Dropout(0.2))

        model.add(LSTM(
            train_X.shape[2],
            return_sequences=False))
        model.add(Dropout(0.2))

        model.add(Dense(
            output_dim=train_X.layers[3]))
        model.add(Activation("linear"))

        start = time.time()
        model.compile(loss="mse", optimizer="rmsprop")
        print("> Compilation Time : ", time.time() - start)














        # model.compile(loss='mse', optimizer='adam')
        model.fit(train_X, train_y, epochs=self.epochs, batch_size=self.batch_size, verbose=1, shuffle=False)
    
        return model

