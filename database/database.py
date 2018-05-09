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
        asset_names = []
        asset_symbols = []
        market_ids = []
        

        for i in range(0, len(markets)):
    
            asset_collection = db.collection(u'users/' + user_id + '/markets/' + markets[i] + '/assets').get()

            for asset in asset_collection:

                asset_dict = asset.to_dict()
                asset_ids.append(str(asset_dict['assetId']))
                asset_names.append(str(asset_dict['name']))
                asset_symbols.append(str(asset_dict['symbol']))
                market_ids.append(str(asset_dict['marketId']))

        data = {'asset_id': asset_ids, 'asset_name': asset_names, 'asset_symbol': asset_symbols,'market_id': market_ids}
        assets = pandas.DataFrame(data=data)
        print(assets)
        return assets


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

    def store_short_term_predictions(self, user_id, market_id, asset_id, series):
        
        test_predictions_firestore_collection = db.collection('users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id + '/short_term_predictions')

        for i in range(0, len(series['date'])):
            print(series['date'][i])
            test_predictions_firestore_collection.document(series['date'][i]).set({
                'date': str(series['date'][i]),
                'predicted_close': float(series['short_term_prediction'][i])
            })

        print('test_predictions successfully stored in the firestore database')



    def store_short_term_predictions_percentage(self):

        test_predictions_firestore_collection = db.collection('users/'+ self.user_id +'/markets/'+ self.market_id + '/assets/' + self.asset_id + '/short_term_predictions_percentage')

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

    
    def store_short_term_prediction(self, user_id, market_id, asset_id, change):
        
        asset_document = db.document('users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id)

        asset_document.update({
            'short_term_prediction': change
        })

        print('test_predictions have been written to firebase.')


    def store_short_term_test_predictions(self, user_id, market_id, asset_id, series):
        
        test_predictions_firestore_collection = db.collection('users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id + '/short_term_test_predictions')

        for i in range(0, len(series['date'])):
            print(series['date'][i])
            test_predictions_firestore_collection.document(series['date'][i]).set({
                'date': str(series['date'][i]),
                'predicted_close': float(series['short_term_prediction'][i])
            })

        print('test_predictions successfully stored in the firestore database')


    def store_series_to_firestore(self, user_id, asset_id, asset_name, asset_symbol, market_id, series):
        print('______________________________________')
        print(series)
        series_firestore_collection = db.collection('users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id + '/series')
        
        dates = []
        closes = []
        
        if (len(series) > 250):

            for i in range(0, 200):
                dates.append(series['date'][i])
                closes.append(series['close'][i])

        if (len(series) < 251):
            
            for i in range(0, len(series)):
                dates.append(series['date'][i])
                closes.append(series['close'][i])

        data = {'date': dates, 'close': closes}
        
        short_series = pandas.DataFrame(data=data)

        for i in range(0, len(short_series)):

            series_firestore_collection.document(short_series['date'][i]).set({
                'name': asset_name,
                'symbol': asset_symbol,
                'date': str(short_series['date'][i]),
                'close': float(short_series['close'][i])
            })
