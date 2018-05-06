import pandas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Import a custom service account generated at Firebase.com and initialization of the firebase backend
cred = credentials.Certificate('./database/service_account.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


class Database:
    
    #################
    ### Variables ###
    #################
    user_id = None
    market_id = None
    asset_id = None
    

    ###################
    ### Constructor ###
    ###################
    def __init__(self):
    
        print('Database connection established')


    #################
    ### Functions ###
    #################
    def fetch_markets(self, user_id):

        markets = []
        market_collection = db.collection('users/' + user_id + '/markets').get()

        for market in market_collection:
            
            market_dict = market.to_dict()
            markets.append(str(market_dict[u'marketId']))

        return markets


    def fetch_assets(self, user_id, markets):

        asset_ids = []
        market_ids = []
        
        for i in range(0, len(markets)):
    
            asset_collection = db.collection(u'users/' + user_id + '/markets/' + markets[i] + '/assets').get()

            for asset in asset_collection:

                asset_dict = asset.to_dict()
                asset_ids.append(str(asset_dict[u'assetId']))
                market_ids.append(str(asset_dict[u'marketId']))

        data = {'asset_id': asset_ids, 'market_id': market_ids}
        
        return pandas.DataFrame(data=data)


    def fetch_series(self, user_id, market_id, asset_id):
        
        dates = []
        closes = []

        series_collection = db.collection('users/' + user_id + '/markets/' + market_id + '/assets/' + asset_id + '/series').get()

        for entry in series_collection:

            entry_dict = entry.to_dict()
            dates.append(str(entry_dict[u'date']))
            closes.append(float(entry_dict[u'close']))
        
        data = {'date': dates, 'close': closes}
        
        return pandas.DataFrame(data=data)
    

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



    def store_short_term_test_predictins(self, user_id, market_id, asset_id, series):
        
        test_predictions_firestore_collection = db.collection(u'users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id + '/short_term_test_predictions')

        for i in range(0, len(series['date'])):
            print(series['date'][i])
            test_predictions_firestore_collection.document(series['date'][i]).set({
                'date': str(series['date'][i]),
                'predicted_close': float(series['short_term_prediction'][i])
            })

        print('test_predictions successfully stored in the firestore database')
