import numpy as np
import matplotlib.pyplot as plt
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import datetime
from keras import backend as K
import tensorflow as tf
import keras.backend.tensorflow_backend
from math_library.math_library import Math_Library
from alphavantage.alphavantage import AlphaVantage
from database.database import Database
import time
from test_series.sine_series import Sine_Series
from test_series import Linear_Series
from data_import import Data_Import
from visualization import Visualization
from prediction import Prediction
from model import Model
from model import Linear_Model
from model import Sine_Model
from model import Lstm_Model

print(' -------------------------------- ')
print(' ##    #  ######  #   #  #######  ')
print(' # #   #  #        # #      #     ')          
print(' #  #  #  ######    #       #     ') 
print(' #   # #  #        # #      #     ')
print(' #    ##  ######  #   #     #     ')
print(' -------------------------------- ')

# class Core:
    
#     user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'
#     db = Database()

#     def execute(self):
        
#         # markets = self.db.fetch_markets(self.user_id)
#         # assets = self.db.fetch_assets(self.user_id, markets)

#         # for i in range(0, len(assets)):

#             # alphaVantage = AlphaVantage()
            
#             # series = alphaVantage.fetch_asset_from_alpha_vantage(self.user_id, assets['asset_id'][i], assets['asset_name'][i], assets['asset_symbol'][i], assets['market_id'][i])

#             # self.db.deleteCollection(self.user_id, assets['market_id'][i], assets['asset_id'][i], 'short_term_predictions')
#             # self.db.deleteCollection(self.user_id, assets['market_id'][i], assets['asset_id'][i], 'short_term_test_predictions')
            

#             # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], model.execute(series, 60))
#             self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], model.execute(series, 50))
#             # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], model.execute(series, 40))
#             # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], model.execute(series, 30))
#             # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], model.execute(series, 20))
#             # self.db.store_short_term_test_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], model.execute(series, 10))
#             self.db.store_short_term_predictions(self.user_id, assets['market_id'][i], assets['asset_id'][i], model.execute(series, 0))
#             self.db.store_short_term_prediction(self.user_id, assets['market_id'][i], assets['asset_id'][i], Math_Library().percentage_change(model.initial_value, model.final_value))            
#             del model    

# Core().execute()   
    # x_train, y_train, x_test, y_test = Data_Import().load_data(df, 50, False)


if __name__=='__main__':
    
    global_start_time = time.time()
    epochs  = 1
    seq_len = 50

    print('> Loading data... ')
    
    df = Sine_Series().create_series()
    scaler = MinMaxScaler(feature_range=(0, 1))

    # model = Sine_Model()
    model = Lstm_Model()
    model = model.build_model()



    value_scaled = scaler.fit_transform(pandas.DataFrame(df['value'][0:1000]))
    date_scaled = scaler.fit_transform(pandas.DataFrame(df['date'][0:1000]))


    model.fit(value_scaled, df['date'][0:1000], epochs=100, batch_size=512)



    prediction = model.predict(date_scaled, batch_size=1)
    test = model.predict(df['value'][0:1000], batch_size=1)


    prediction = scaler.inverse_transform(prediction)
    test = scaler.inverse_transform(test)







    plt.plot(df['value'][0:1000], label='real')
    plt.plot(test, label='test')
    plt.plot(prediction, label='prediction')
    plt.legend()
    plt.show()

















    # model.fit(x_train, y_train, batch_size=512, epochs=epochs, validation_split=0.05)
    

    # predictions = Prediction().predict_sequences_multiple(model, x_test, seq_len, 50)
    # predictions = Prediction().predict_sequence_full(model, x_test, seq_len)
    # predictions = Prediction().predict_point_by_point(model, x_test)        

    # print('Training duration (s) : ', time.time() - global_start_time)
    # Visualization().plot_results_multiple(predictions, y_test, 50)

    # Visualization().display_series(df)


