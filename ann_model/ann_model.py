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


class ANN_Model:
    
    scaler = None
    future_dates = []

    # Constructor
    def __init__(self):
        print('ANN_Model created')
        
    
    def execute(self, series, lag):
        
        reduced_series = self.reduce_series(series, lag)
        normalized_closes = self.normalize_data(reduced_series)
        ann_input = self.create_train_and_test_sets(normalized_closes)
        ann_model = self.create_core_model(ann_input)
        normalized_short_term_predictions = self.generate_short_term_predictions(ann_input, ann_model)
        denormalized_predicted_short_term_closes = self.inverse_predictions(normalized_short_term_predictions)

        return denormalized_predicted_short_term_closes


    def reduce_series(self, series, lag):
        
        self.future_dates = []
        dates = []
        closes = []

        for i in range(0, len(series) - lag):
        
            closes.append(series['close'][i])
            dates.append(series['date'][i]) 

        for i in range(len(series) - lag, len(series) - lag + 10):
            if(series['date'][i]):
                self.future_dates.append(series['date'][i])
        
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

        # train_size = len(series)
        # train_close_values = series['close'][ 0 : train_size, :]

        # print(train_close_values)
        # # self.train_date_values = series[0:train_size]
        return self.create_dataset(series, 1)

        
        # '''
        # Splitting up the dataset in a train and a test dataset
        # '''

        # train_size = int(len(self.dataset))
        # test_size = len(self.dataset) - train_size

        # self.train_close_values = self.dataset[ 0 : train_size, :]
        # self.test_close_values = self.dataset[ train_size : len(self.dataset), :]

        # self.train_date_values = self.dates[0:train_size]
        # self.test_date_values = self.dates[train_size:len(self.dates)]

        # self.trainX, self.trainY = self.create_dataset(series, 1)
        # testX, testY = create_dataset(test_close_values, look_back)



    def create_core_model(self, series):

        model = Sequential()
        model.add(Dense(12, input_dim = 1, activation = 'relu'))
        model.add(Dense(8, activation = 'relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(series['close_lag_0'], series['close_lag_1'], epochs=400, batch_size=1, verbose=2)
        
        return model


    def generate_short_term_predictions(self, series, model):
    
        short_term_predictions = []
        float_short_term_predictions = []
        input = series['close_lag_1'][len(series['close_lag_1'])-1]
        short_term_predictions.append(model.predict([input])[0])
        
        for i in range(1, 10):
            short_term_predictions.append(model.predict(short_term_predictions[i-1])[0])

        for i in range(0, len(short_term_predictions)):
            float_short_term_predictions.append(short_term_predictions[i][0])

        data = {'date': self.future_dates, 'short_term_prediction': float_short_term_predictions}
        return pandas.DataFrame(data=data)



    def inverse_predictions(self, series):
        
        # self.train_predictions = self.scaler.inverse_transform(self.train_predictions)
        # self.trainY = self.scaler.inverse_transform([self.trainY])

        # test_predictions = scaler.inverse_transform(test_predictions)
        # testY = scaler.inverse_transform([testY])
        
        short_term_predictions = self.scaler.inverse_transform([series['short_term_prediction']])
        data = {'date': series['date'], 'short_term_prediction': short_term_predictions[0]}

        return pandas.DataFrame(data=data)
        # testY = scaler.inverse_transform([testY])

        # calculate root mean squared error
        # trainScore = math.sqrt(mean_squared_error(trainY[0], train_predictions[:,0]))
        # print('Train Score: %.2f RMSE' % (trainScore))
        # testScore = math.sqrt(mean_squared_error(testY[0], test_predictions[:,0]))
        # print('Test Score: %.2f RMSE' % (testScore))
    

