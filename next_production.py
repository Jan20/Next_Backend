import firebase_admin
import numpy as numpy
from firebase_admin import credentials
from firebase_admin import firestore
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


print(' ------------------------------- ')
print(' ##    #  ######  #    #  ###### ')
print(' # #   #  #        #  #     #    ')          
print(' #  #  #  ######    #       #    ') 
print(' #   # #  #        #  #     #    ')
print(' #    ##  ######  #    #    #    ')
print(' ------------------------------- ')


# Import a custom service account generated at Firebase.com
cred = credentials.Certificate('./service_account.json')

# Initialization of the firebase backend
firebase_admin.initialize_app(cred)

db = firestore.client()

# Deprecated
#__________________________________________________________
if keras.backend.tensorflow_backend._SESSION:

   tf.reset_default_graph() 
   keras.backend.tensorflow_backend._SESSION.close()
   keras.backend.tensorflow_backend._SESSION = None
#__________________________________________________________

class Next:
    
    # Variables

    user_id = None
    market_id = None
    asset_id = None

    scaler = None
    dataset = []
    dates = []
    model = None

    trainX = []
    trainY = []
    dataX = None
    dataY = None
    train_predictions = None
    test_predictions = None
    look_back = 1

    # Train and Test Sets
    train_close_values = None
    test_close_values = None
    train_date_values = None
    test_date_values = []

    # Constructor
    def __init__(self, user_id, market_id, asset_id):
        self.user_id = user_id
        self.market_id = market_id
        self.asset_id = asset_id


    def retrieve_data_from_firestore(self):

        '''
        Function that is solely used to retrieve data from the
        Firestore-backend defiend within a corresponding service_account.json
        file. Finally, the data are converted in a pandas dataframe
        '''

        asset_collection = db.collection('users/' + self.user_id + '/markets/' + self.market_id + '/assets/' + self.asset_id + '/series').get()

        self.dates = []
        self.dataset = []

        for asset in asset_collection:
            asset_dict = asset.to_dict()
            self.dates.append(str(asset_dict[u'date']))
            self.dataset.append(float(asset_dict[u'close']))
        
        for i in range(1,10):
            self.dates.append(str(datetime.date.today() + datetime.timedelta(days=1)))


        print(self.test_date_values)
        self.dataset = pandas.DataFrame(data=self.dataset)
        print(self.dataset)


    def normalize_data(self):
        
        '''
        Mapping of the dataframe entries to a value between -1 and 1.
        '''

        numpy.random.seed(7)

        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.dataset = self.scaler.fit_transform(self.dataset)
        

    def create_dataset(self, dataset, look_back = 1):
    
        '''
        
        Creates a dataset from an existing one with an optional look_back period.
        
        
        '''

        self.look_back = 1
        self.dataX, self.dataY = [], []
        
        for i in range( len(self.dataset) - self.look_back - 1 ):
        
            self.dataX.append( self.dataset[ i: ( i + self.look_back ), 0 ] )
            self.dataY.append( self.dataset[ i + self.look_back, 0 ] )

        return numpy.array( self.dataX ), numpy.array( self.dataY )


    def create_train_and_test_sets(self):
        
        '''
        Splitting up the dataset in a train and a test dataset
        '''

        train_size = int(len(self.dataset))
        test_size = len(self.dataset) - train_size

        self.train_close_values = self.dataset[ 0 : train_size, :]
        self.test_close_values = self.dataset[ train_size : len(self.dataset), :]

        self.train_date_values = self.dates[0:train_size]
        self.test_date_values = self.dates[train_size:len(self.dates)]

        self.trainX, self.trainY = self.create_dataset(self.train_close_values, self.look_back)
        # testX, testY = create_dataset(test_close_values, look_back)
















    def create_core_model(self):
        
        '''

        Function in which the core artificial neuronal network is defined
        and trained.

        '''
        if keras.backend.tensorflow_backend._SESSION:
            print('_____________________________________________________________________________________________________________ ')
            tf.reset_default_graph() 
            keras.backend.tensorflow_backend._SESSION.close()
            keras.backend.tensorflow_backend._SESSION = None
        K.clear_session() # removing session, it will instance another
        self.model = None

        self.model = Sequential()
        self.model.add(Dense(12, input_dim= self.look_back, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        print('________________________________________________________TRAIN X______________________________________________________________________')
        print(self.trainX)
        print('________________________________________________________TRAIN Y______________________________________________________________________')
        print(self.trainY)
        self.model.fit(self.trainX, self.trainY, epochs=400, batch_size=1, verbose=2)

        '''

        Function, responsible for creating short_term predictions of
        upcoming market movements.

        '''
        self.test_predictions = None
        self.test_predictions = numpy.array( self.trainX[ len(self.trainX) - 1 ])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[0])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[1])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[2])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[3])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[4])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[5])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[6])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[7])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[8])
        self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[9])
        
        tf.reset_default_graph()
        keras.backend.tensorflow_backend._SESSION.close()
        keras.backend.tensorflow_backend._SESSION = None
        K.clear_session()
        tf.reset_default_graph() # for being sure
        K.clear_session() # removing session, it will instance another
        self.model = None
        self.model = Sequential()





# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras.layers import Embedding
# from keras.layers import LSTM

# model = Sequential()
# model.add(Embedding(max_features, output_dim=256))
# model.add(LSTM(128))
# model.add(Dropout(0.5))
# model.add(Dense(1, activation='sigmoid'))

# model.compile(loss='binary_crossentropy',
#               optimizer='rmsprop',
#               metrics=['accuracy'])

# model.fit(x_train, y_train, batch_size=16, epochs=10)
# score = model.evaluate(x_test, y_test, batch_size=16)













    # def validations(self):
    #     train_predictions = self.model.predict(trainX)


    # def create_short_term_predictions(self):
    
        # '''

        # Function, responsible for creating short_term predictions of
        # upcoming market movements.

        # '''
        # self.test_predictions = None
        # self.test_predictions = numpy.array( self.trainX[ len(self.trainX) - 1 ])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[0])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[1])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[2])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[3])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[4])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[5])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[6])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[7])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[8])
        # self.test_predictions = numpy.append( self.test_predictions, self.model.predict(self.test_predictions)[9])
        
        # tf.reset_default_graph()
        # keras.backend.tensorflow_backend._SESSION.close()
        # keras.backend.tensorflow_backend._SESSION = None
        # K.clear_session()
        # tf.reset_default_graph() # for being sure
        # K.clear_session() # removing session, it will instance another
        # self.model = None
        # self.model = Sequential()


    def inverse_predictions(self):
        
        '''
        
        Invert predictions from a -1 to 1 scale to the according
        real-world representation.

        '''
        
        # self.train_predictions = self.scaler.inverse_transform(self.train_predictions)
        # self.trainY = self.scaler.inverse_transform([self.trainY])

        # test_predictions = scaler.inverse_transform(test_predictions)
        # testY = scaler.inverse_transform([testY])

        self.test_predictions = self.scaler.inverse_transform([self.test_predictions])
        # testY = scaler.inverse_transform([testY])

        # calculate root mean squared error
        # trainScore = math.sqrt(mean_squared_error(trainY[0], train_predictions[:,0]))
        # print('Train Score: %.2f RMSE' % (trainScore))
        # testScore = math.sqrt(mean_squared_error(testY[0], test_predictions[:,0]))
        # print('Test Score: %.2f RMSE' % (testScore))
    

    def store_short_term_predictins(self):
        
        '''
        
        Writing Data to the Firebase Database
        
        '''

        # train_predictions_firestore_collection = db.collection(u'users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi/train_predictions')

        # for i in range(1, len(self.train_predictions)):
        #     train_predictions_firestore_collection.document(self.train_date_values[i]).set({
        #         'date': str(self.train_date_values[i]),
        #         'predicted_close': float(self.train_predictions[i]) 
        #     })

        # print('trian_predictions have been written to firebase.')

        # Test Predictions

        test_predictions_firestore_collection = db.collection(u'users/'+ self.user_id +'/markets/'+ self.market_id + '/assets/' + self.asset_id + '/short_term_predictions')
        self.test_date_values = []

        for i in range( 1, 11):
            self.test_date_values.append(str(datetime.date.today() + datetime.timedelta(days=i)))

        print('--- final predictions ---')
        print(self.test_date_values)
        print(self.test_predictions)

        for i in range(2, len(self.test_predictions[0])+1):
            print(str(self.test_date_values[i-2]))
            test_predictions_firestore_collection.document(self.test_date_values[i-2]).set({
                'date': str(self.test_date_values[i-2]),
                'predicted_close': float(self.test_predictions[0][i-1])
            })

        print('test_predictions have been written to firebase.')


    def store_short_term_predictions_percentage(self):

        test_predictions_firestore_collection = db.collection(u'users/'+ self.user_id +'/markets/'+ self.market_id + '/assets/' + self.asset_id + '/short_term_predictions_percentage')

        self.test_date_values = []

        for i in range( 1, 11):
            self.test_date_values.append(str(datetime.date.today() + datetime.timedelta(days=i)))

        print('--- final predictions ---')
        print(self.test_date_values)
        print(self.test_predictions)

        for i in range(2, len(self.test_predictions[0])+1):
            print(str(self.test_date_values[i-2]))
            test_predictions_firestore_collection.document(self.test_date_values[i-2]).set({
                'date': str(self.test_date_values[i-2]),
                'predicted_close': ((float(self.test_predictions[0][i-1])-float(self.test_predictions[0][i-2])) / float(self.test_predictions[0][i-2])) * 100
            })

        print('test_predictions have been written to firebase.')

    
    def store_short_term_prediction(self):

        asset_document = db.document(u'users/'+ self.user_id +'/markets/'+ self.market_id + '/assets/' + self.asset_id)

        self.test_date_values = []

        for i in range( 1, 11):
            self.test_date_values.append(str(datetime.date.today() + datetime.timedelta(days=i)))

        print('--- final predictions ---')
        print(self.test_date_values)
        print(self.test_predictions)

        short_term_prediction = ((float(self.test_predictions[0][len(self.test_predictions[0])-1])-float(self.test_predictions[0][1])) / float(self.test_predictions[0][1])) * 100

        asset_document.update({
            'short_term_prediction': short_term_prediction
        })
        self.model = None
        print('test_predictions have been written to firebase.')


class Execution_Environment:
    
    def start(self):
        
        user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'
        markets = []

        market_collection = db.collection(u'users/' + user_id + '/markets').get()

        for market in market_collection:
            
            market_dict = market.to_dict()
            markets.append(str(market_dict[u'marketId']))
        

        for i in range(0, len(markets)):

            assets = []
            asset_collection = db.collection(u'users/' + user_id + '/markets/' + markets[i] + '/assets').get()

            print(asset_collection)

            for asset in asset_collection:
                asset_dict = asset.to_dict()
                assets.append(str(asset_dict[u'assetId']))
            
            for j in range(0, len(assets)):
                
                t = Next(user_id, markets[i], assets[j])
                t.retrieve_data_from_firestore()
                t.normalize_data()
                t.create_train_and_test_sets()
                t.create_core_model()
                # t.create_short_term_predictions()
                t.inverse_predictions()
                t.store_short_term_predictins()
                t.store_short_term_predictions_percentage()
                t.store_short_term_prediction()
                del t

execution_environment = Execution_Environment()
execution_environment.start()