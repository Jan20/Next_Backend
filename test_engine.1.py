import numpy as numpy
import matplotlib.pyplot as plt
import pandas
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
from ann_model.ann_model import ANN_Model
from alphavantage.alphavantage import AlphaVantage

from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from alphavantage.alphavantage import AlphaVantage



print(' -------------------------------- ')
print(' ##    #  ######  #   #  #######  ')
print(' # #   #  #        # #      #     ')          
print(' #  #  #  ######    #       #     ') 
print(' #   # #  #        # #      #     ')
print(' #    ##  ######  #   #     #     ')
print(' -------------------------------- ')

class Test_Engine:
    
    user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'
    db = Database()

    def execute(self):
        
        markets = self.db.fetch_markets(self.user_id)
        assets = self.db.fetch_assets(self.user_id, markets)

        for i in range(0, len(assets)):
            alphaVantage = AlphaVantage()
            series = alphaVantage.fetchAssetFromAlphaVantage(self.user_id, assets['asset_id'][i], assets['asset_name'][i], assets['asset_symbol'][i], assets['market_id'][i])

            scaler = MinMaxScaler(feature_range=(0, 1))
            series_new = DataFrame(series['close'])
            scaled = scaler.fit_transform(series_new)
            # frame as supervised learning
            reframed = series_to_supervised(scaled, 1, 1)
            # drop columns we don't want to predict
            # reframed.drop(reframed.columns[[9,10,11,12,13,14,15]], axis=1, inplace=True)
            # print(reframed.head())
            
       
            # test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
            # # invert scaling for forecast
            # inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
            # inv_yhat = scaler.inverse_transform(inv_yhat)
            # inv_yhat = inv_yhat[:,0]
            # # invert scaling for actual
            # test_y = test_y.reshape((len(test_y), 1))
            # inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
            # inv_y = scaler.inverse_transform(inv_y)
            # inv_y = inv_y[:,0]
            # # calculate RMSE
            # rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
            # print('Test RMSE: %.3f' % rmse)




test_engine = Test_Engine()
test_engine.execute()   


