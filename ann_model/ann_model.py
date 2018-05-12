import pandas
from pandas import DataFrame
import numpy as numpy
import matplotlib.pyplot as plt
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
import datetime
from keras import backend as K
import tensorflow as tf
import keras.backend.tensorflow_backend
from database.database import Database
from pipeline.pipeline import Pipeline

class ANN_Model:
    
    epochs=48

    db = Database()
    scaler = None
    series = None
    lag = 0
    initial_value = None
    final_value = None
    dates = []
    closes = []

    def execute(self, series, lag):
        
        self.series = series
        self.lag = lag
        pipeline = Pipeline()

        reduced_series = pipeline.reduce_series(series, lag)
        self.dates = pipeline.get_dates(reduced_series)
        normalize_series = pipeline.normalize_data(reduced_series)

        self.closes = normalize_series[0]
        supervised_series = pipeline.series_to_supervised(normalize_series, 1, 1, True)
        train_X, train_y, test_X, test_y = pipeline.create_train_and_test_sets(supervised_series)
        ann_model = self.create_core_model(train_X, train_y, test_X, test_y)
        normalized_short_term_predictions = self.generate_short_term_predictions(ann_model, test_X)
        denormalized_predicted_short_term_closes = pipeline.inverse_predictions(normalized_short_term_predictions)
        
        return denormalized_predicted_short_term_closes



    def create_core_model(self, train_X, train_y, test_X, test_y):
        
        if keras.backend.tensorflow_backend._SESSION:
            tf.reset_default_graph() 
            keras.backend.tensorflow_backend._SESSION.close()
            keras.backend.tensorflow_backend._SESSION = None
        
        K.clear_session() # removing session, it will instance another
        model = None

        # model = Sequential()
        # model.add(Dense(24, input_dim = 1, activation = 'relu'))
        # model.add(Dense(8, activation = 'relu'))
        # model.add(Dense(1))
        # model.compile(loss='mean_squared_error', optimizer='adam')
        # model.fit(series['close_lag_0'], series['close_lag_1'], epochs=3, batch_size=1, verbose=2)

        # design network
        model = Sequential()
        model.add(LSTM(12, input_shape=(train_X.shape[1], train_X.shape[2])))
        # model.add(Dense(24, input_dim = 1, activation = 'relu'))
        # model.add(Dense(8, activation = 'relu'))
        # model.add(Dense(24, input_dim = 1, activation = 'relu'))
        # model.add(Dense(8, activation = 'relu'))
        model.add(Dense(1))
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')
        # fit network
        history = model.fit(train_X, train_y, epochs=self.epochs, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
        # plot history
        # pyplot.plot(history.history['loss'], label='train')
        # pyplot.plot(history.history['val_loss'], label='test')
        # pyplot.legend()
        # pyplot.show()
        
        return model


    def generate_short_term_predictions(self, model, test_X):
        self.initial_value = test_X
        
        t = numpy.zeros((1,1,1))
        print('#### INITIAL VALUE #####')
        print(test_X)
        print('#### ------------- #####')
        t[0][0][0] = test_X
        print(t)
        print(t.shape)
        short_term_predictions = []
        short_term_predictions.append(model.predict(t))

        for i in range(1, 10):
            temp = numpy.zeros((1,1,1))
            temp[0][0][0] = short_term_predictions[i-1]
            d = model.predict(temp)
            short_term_predictions.append(d[0][0])
        
        self.final_value = short_term_predictions[len(short_term_predictions)-1]

        dates = []

        if (self.lag > 0):
            print('#########################Dates#######################')
            for i in range(0,10):
                print(self.dates[i])
                dates.append(self.dates[i])

        if (self.lag == 0):
            for i in range(1,11):
                dates.append(str(datetime.date.today() + datetime.timedelta(days=i)))

        print(short_term_predictions)
        print(pandas.DataFrame(data={'date': dates, 'short_term_prediction': short_term_predictions}))
        return pandas.DataFrame(data={'date': dates, 'short_term_prediction': short_term_predictions})

    def calculate_change(self):

        change = ((self.final_value - self.initial_value) / self.initial_value) * 100
        print('#### Change #####')
        print(change[0][0][0])
        print('#### ------------- #####')

        return str(change[0][0][0])


  