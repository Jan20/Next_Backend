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
    epochs = 100
    batch_size = 1024
    db = Database()

    initial_value = None
    final_value = None

    def execute(self, series, lag):

        pipeline = Pipeline()
        predictionGenerator = PredictionGenerator()

        reduced_series = pipeline.reduce_series(series, lag)
        lagged_series = pipeline.get_lagged_series(series, lag)
        normalized_series = pipeline.normalize_data(reduced_series)
        supervised_series = pipeline.series_to_supervised(normalized_series, 1, 1, True)
        train_X, train_y, test_X, test_y = pipeline.create_train_and_test_sets(supervised_series)
        ann_model = self.create_core_model(train_X, train_y, test_X, test_y)
        normalized_short_term_predictions = predictionGenerator.generate_short_term_predictions(ann_model, test_X, lag, lagged_series)
        
        # Ugly
        self.initial_value = predictionGenerator.initial_value
        self.final_value = predictionGenerator.final_value
        
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
        model = Sequential()
        # model.add(Dense(12, input_shape=(train_X.shape[0][0][0], train_X.shape[1]), activation='relu'))
        # model.add(Dense(8, activation='relu'))
        # model.add(Dense(1, activation='sigmoid'))
        model.add(LSTM(4, input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mse', optimizer='adam')
        model.fit(train_X, train_y, epochs=self.epochs, batch_size=self.batch_size, verbose=1, shuffle=False)
    
        return model

