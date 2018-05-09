import pandas
import numpy as numpy
import matplotlib.pyplot as plt
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import datetime
from keras import backend as K
import tensorflow as tf
import keras.backend.tensorflow_backend
from database.database import Database

class ANN_Model:
    
    db = Database()
    scaler = None
    series = None
    lag = 0
    initial_value = None
    final_value = None

    def execute(self, series, lag):
        
        self.series = series
        self.lag = lag

        reduced_series = self.reduce_series(series, lag)
        normalized_closes = self.normalize_data(reduced_series)
        ann_input = self.create_train_and_test_sets(normalized_closes)
        ann_model = self.create_core_model(ann_input)
        normalized_short_term_predictions = self.generate_short_term_predictions(ann_input, ann_model)
        denormalized_predicted_short_term_closes = self.inverse_predictions(normalized_short_term_predictions)
        return denormalized_predicted_short_term_closes


    def reduce_series(self, series, lag):

        dates = []
        closes = []

        for i in range(0, len(series['date']) - lag):

            dates.append(series['date'][i])
            closes.append(series['close'][i])

        data = {'date': dates, 'close': closes}
        
        return pandas.DataFrame(data=data)
        

    def normalize_data(self, series):
        
        numpy.random.seed(7)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
        close_dataframe = pandas.DataFrame(data=series['close'])
        closes = self.scaler.fit_transform(close_dataframe)

        closes_array = [row[0] for row in closes]

        data = {'date': series['date'], 'close': closes_array}
        return pandas.DataFrame(data=data)


    def create_dataset(self, series, look_back):

        dates = []
        closes_lag_0 = []
        closes_lag_1 = []

        for i in range(0, len(series['close']) - look_back):
            
            dates.append(series['date'][i])
            closes_lag_0.append(series['close'][i])
            closes_lag_1.append(series['close'][i+1])

        data = {'date': dates, 'close_lag_0': closes_lag_0, 'close_lag_1': closes_lag_1}
        return pandas.DataFrame(data=data)


    def create_train_and_test_sets(self, series):

        return self.create_dataset(series, 1)


    def create_core_model(self, series):

        look_back = 1
        batch_size = 1

        # model = Sequential()
        # model.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True))
        # model.add(Dense(1))
        # model.compile(loss='mean_squared_error', optimizer='adam')
        # for i in range(len(series['date'])):
        #     model.fit(series[i]['close_lag_0'], series[i]['close_lag_1'], epochs=1, batch_size=batch_size, verbose=2, shuffle=False)
        #     model.reset_states()


        model = Sequential()
        model.add(Dense(12, input_dim = 1, activation = 'relu'))
        model.add(Dense(8, activation = 'relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(series['close_lag_0'], series['close_lag_1'], epochs=3, batch_size=1, verbose=2)
        
        return model


    def generate_short_term_predictions(self, series, model):
    
        print('___________________________ERROR____________________________________________________________________')
        print(series['close_lag_0'])
        print (series)

        input = series['close_lag_0'][0]
        self.initial_value = input

        short_term_predictions = []
        short_term_predictions.append(model.predict([input]))

        for i in range(1, 10):
            short_term_predictions.append(model.predict(short_term_predictions[i-1])[0])
        
        float_short_term_predictions = []
        
        for i in range(0, len(short_term_predictions)):
            float_short_term_predictions.append(short_term_predictions[i][0])

        self.final_value = float_short_term_predictions[len(short_term_predictions)-1]

        
        dates = []

        if (self.lag > 0):
            for i in range(1,11):
                dates.append(self.series['date'][i])

        if (self.lag == 0):
            for i in range(1,11):
                dates.append(str(datetime.date.today() + datetime.timedelta(days=i)))

        print(float_short_term_predictions)
        
        data = {'date': dates, 'short_term_prediction': float_short_term_predictions}

        return pandas.DataFrame(data=data)

    def calculate_change(self):
        
        change = ((self.final_value - self.initial_value) / self.initial_value) * 100
        
        print('__________change____________')
        print(change)

        change = str(change)

        return change


    def inverse_predictions(self, series):
        
        short_term_predictions = self.scaler.inverse_transform([series['short_term_prediction']])
        data = {'date': series['date'], 'short_term_prediction': short_term_predictions[0]}
        print('Inverted predictions')
        print(data)
        return pandas.DataFrame(data=data)


