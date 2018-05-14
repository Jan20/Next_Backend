import pandas
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler

class Pipeline:

    ###############
    ## Variables ##
    ###############

    scaler = MinMaxScaler(feature_range=(0, 1))
    
    ###############
    ## Functions ##
    ###############
    
    def get_lagged_series(self, series, lag):
            
        dates, closes = [], []

        if lag > 0:
            for i in range(lag - 10, lag):
                
                dates.append(series['date'][i])
                closes.append(series['close'][i])

        return pandas.DataFrame(data={'date': dates, 'close': closes})


    def reduce_series(self, series, lag):

        dates, closes = [], []

        for i in range(0, len(series) - lag):

            dates.append(series['date'][i])
            closes.append(series['close'][i])

        return pandas.DataFrame(data={'date': dates, 'close': closes})

        
    # Tested
    def normalize_data(self, series):
        
        return self.scaler.fit_transform(DataFrame(series['close']))

    # convert series to supervised learning
    def series_to_supervised(self, data, n_in=1, n_out=1, dropnan=True):
    
        n_vars = 1 if type(data) is list else data.shape[1]
    
        df = DataFrame(data)

        cols, names = list(), list()
        
        # input sequence (t-n, ... t-1)
        
        for i in range(n_in, 0, -1):
        
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        
        # forecast sequence (t, t+1, ... t+n)
        
        for i in range(0, n_out):
        
            cols.append(df.shift(-i))
        
            if i == 0:
                names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
        
        # put it all together
        
        agg = concat(cols, axis=1)
        agg.columns = names
        
        # drop rows with NaN values
        
        if dropnan:
            agg.dropna(inplace=True)
        
        return agg



    def create_train_and_test_sets(self, reframed):

        values = reframed.values

        print('---------- TEST --------------------')
        print(values[0:10,0:10])
        print('---------- // TEST --------------------')

        n_train_hours = len(reframed)
        train = values[:n_train_hours, :]
        test = values[0:1, :]
        # split into input and outputs
        train_X, train_y = train[:, :-1], train[:, -1]
        test_X, test_y = test[:, :-1], test[:, -1]
        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
        test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
        
        print('------------------------ TRAIN X ------------------------')
        print(train_X)
        print('------------------------ TRAIN y ------------------------')
        print(train_y)
        print('------------------------ TEST X ------------------------')
        print(train_y)
        print('------------------------ TEST y ------------------------')
        print(train_y)
        return train_X, train_y, test_X, test_y


    def inverse_predictions(self, series):
        
        print(series)
        short_term_predictions = self.scaler.inverse_transform([series['short_term_prediction']])
        print('Inverted predictions')
        print(short_term_predictions)

        return pandas.DataFrame(data={'date': series['date'], 'short_term_prediction': short_term_predictions[0]})

