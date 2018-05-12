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


            # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.execute(series, 60))
            # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.execute(series, 50))
            # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.execute(series, 40))
            # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.execute(series, 30))
            ann_model = ANN_Model()
            # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.execute(series, 20))
            self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.execute(series, 10))
            self.db.store_short_term_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.execute(series, 0))
            self.db.store_short_term_prediction(self.user_id, assets['market_id'][i], assets['asset_id'][i], ann_model.calculate_change())            
            del ann_model    


test_engine = Test_Engine()
test_engine.execute()   


