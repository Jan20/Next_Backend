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

    #######################
    ### Fetch Functions ###
    #######################

    def fetch_markets(self, user_id):

        markets = []

        for market in db.collection('users/' + user_id + '/markets').get():
            
            market_dict = market.to_dict()
            markets.append(str(market_dict['marketId']))

        return markets


    def fetch_assets(self, user_id, markets):

        market_ids, asset_ids, asset_names, asset_symbols = [], [], [], []

        for i in range(0, len(markets)):

            for asset in db.collection('users/' + user_id + '/markets/' + markets[i] + '/assets').get():

                asset_dict = asset.to_dict()
                asset_ids.append(str(asset_dict['symbol']))
                asset_names.append(str(asset_dict['name']))
                asset_symbols.append(str(asset_dict['symbol']))
                market_ids.append(str(asset_dict['marketId']))

        return pandas.DataFrame(data={'asset_id': asset_ids, 'asset_name': asset_names, 'asset_symbol': asset_symbols,'market_id': market_ids})


    def fetch_series(self, user_id, market_id, asset_id):
        
        dates, values = [], []

        for entry in db.collection('users/' + user_id + '/markets/' + market_id + '/assets/' + asset_id + '/series').get():

            entry_dict = entry.to_dict()
            dates.append(str(entry_dict[u'date']))
            values.append(float(entry_dict[u'value']))
        
        return pandas.DataFrame(data={'date': dates, 'value': values})

    #######################
    ### Write Functions ###
    #######################

    def store_series(self, user_id, market_id, asset_id, series_name, series):
        
        firestore_collection = db.collection('users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id + '/' + series_name)

        if (series_name == 'series'):

            dates, values = [], []

            for entry in firestore_collection.get():

                entry_dict = entry.to_dict()
                dates.append(entry_dict['date'])
                values.append(entry_dict['value'])

            entries = pandas.DataFrame(data={'date': dates, 'value': values})
            
            series = series[(~series.date.isin(entries.date))]


            print('------------- Resulting Series ---------------')
            print(series)


            for i in range(0, len(series['date'])):
        
                print(str(series['date'][i]))

                firestore_collection.document(series['date'][i]).set({
                
                    'date': str(series['date'][i]),
                    'value': float(series['value'][i])
            
                })

        print('Series has been saved at Firestore.')


    def store_value(self, user_id, market_id, asset_id, value_name, value):
        
        asset_document = db.document('users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id)

        asset_document.update({
        
            value_name: value
        
        })

        print('test_predictions have been written to firebase.')


    def store_short_term_predictions(self, user_id, market_id, asset_id, series):
        
        test_predictions_firestore_collection = db.collection('users/'+ user_id +'/markets/'+ market_id + '/assets/' + asset_id + '/short_term_predictions')

        for i in range(0, len(series['date'])):

            test_predictions_firestore_collection.document(series['date'][i]).set({
                'date': str(series['date'][i]),
                'predicted_value': float(series['short_term_prediction'][i])
            })

        print('test_predictions successfully stored in the firestore database')


    def store_short_term_predictions_percentage(self):

        test_predictions_firestore_collection = db.collection('users/'+ self.user_id +'/markets/'+ self.market_id + '/assets/' + self.asset_id + '/short_term_predictions_percentage')

        self.test_date_values = []

        for i in range( 1, 11):
            self.test_date_values.append(str(datetime.date.today() + datetime.timedelta(days=i)))

        for i in range(2, len(self.test_predictions[0])+1):
            print(str(self.test_date_values[i-2]))
            test_predictions_firestore_collection.document(self.test_date_values[i-2]).set({
                'date': str(self.test_date_values[i-2]),
                'predicted_value': ((float(self.test_predictions[0][i-1])-float(self.test_predictions[0][i-2])) / float(self.test_predictions[0][i-2])) * 100
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
                'predicted_value': float(series['short_term_prediction'][i])
            })

        print('test_predictions successfully stored in the firestore database')


    def deleteCollection(self, user_id, market_id, asset_id, collection):

        for entry in db.collection('users/' + user_id + '/markets/' + market_id + '/assets/' + asset_id + '/' + collection).get():
            
            entry_dict = entry.to_dict()
            db.document('users/' + user_id + '/markets/' + market_id + '/assets/' + asset_id + '/' + collection + '/' + entry_dict['date']).delete()

        print(collection + ' collection was successfully deleted.')


    def store_market(self, user_id, market_id, name, symbol):

        data = {'name': name, 'symbol': symbol, 'marketId': market_id}

        db.collection('users/' + user_id + '/markets/' + market_id + '/assets').document(symbol).set(data)



