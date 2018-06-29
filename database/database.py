
import pandas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

# Import a custom service account generated at Firebase.com and initialization of the firebase backend
cred = credentials.Certificate('./database/service_account.json')
firebase_admin.initialize_app(cred)
database = firestore.client()

class Database:

    #################
    ### Variables ###
    #################
    
    user_id = None
    market_id = None
    asset_id = None

    ############
    ## MARKET ##
    ############

    def fetch_markets(self):

        markets = []

        for market in database.collection('markets').get():
            
            market_dict = market.to_dict()
            markets.append(str(market_dict['market_id']))

        print(markets)
        return markets


    def create_market(self, name, category, market_id):

        data = {'name': name, 'category': category, 'market_id': market_id}

        database.collection('markets').document(market_id).set(data)

    ###########
    ## ASSET ##
    ###########

    def fetch_assets(self, market_id):

        dataframe = pandas.DataFrame(columns=['name', 'symbol', 'market_id'])

        for asset in database.collection('markets/' + market_id + '/assets').get():
            
            asset_dict = asset.to_dict()
            dataframe = dataframe.append({'name': asset_dict['name'], 'symbol': asset_dict['symbol'], 'market_id': asset_dict['market_id']}, ignore_index=True)

        print(dataframe)
        return dataframe

    ############
    ## Series ##
    ############

    def fetch_series(self, market_id, asset_id):
        
        dates, values = [], []

        for entry in database.collection('markets/' + market_id + '/assets/' + asset_id + '/series').get():

            entry_dict = entry.to_dict()
            dates.append(str(entry_dict[u'date']))
            values.append(float(entry_dict[u'value']))
        
        return pandas.DataFrame(data={'date': dates, 'value': values})

    
    def create_asset(self, name, symbol, market_id):
        
        data = {'name': name, 'symbol': symbol, 'market_id': market_id}
        
        database.collection('markets/'+ market_id + '/assets').document(symbol).set(data)

        print('a new asset has been created.')
       

    def update_asset(self, market_id, asset_id, value_name, value):
        
        asset_document = database.document('markets/'+ market_id + '/assets/' + asset_id)

        asset_document.update({
        
            value_name: value
        
        })

        print('an existing asset has been updated.')
       

    #############
    ### WRITE ###
    #############
    def fetch_series(self, market_id, symbol):
        
        dataframe = pandas.DataFrame(columns=['date', 'value'])

        for series in database.collection('markets/' + market_id + '/assets/' + symbol + '/series').get():
            
            series_dict = series.to_dict()
            dataframe = dataframe.append({'date': series_dict['date'], 'value': series_dict['value']}, ignore_index=True)

        print(dataframe)
        return dataframe


    def store_series(self, market_id, symbol, series_name, series):
        
        firestore_collection = database.collection('markets/'+ market_id + '/assets/' + symbol + '/' + series_name)

        dataframe = pandas.DataFrame(columns=['date', 'value'])

        for entry in firestore_collection.get():

            entry_dict = entry.to_dict()
            dataframe = dataframe.append({'date': entry_dict['date'], 'value': entry_dict['value']}, ignore_index=True)

        dataframe = series[(~series.date.isin(dataframe.date))]


        for i in range(0, len(dataframe['date'])):

            print(str(dataframe['date'][i]))

            firestore_collection.document(dataframe['date'][i]).set({
            
                'date': str(dataframe['date'][i]),
                'value': float(dataframe['value'][i])
        
            })

        print('Series has been saved at Firestore.')


    def store_short_term_predictions(self, user_id, market_id, asset_id, series):
        
        test_predictions_firestore_collection = database.collection('markets/'+ market_id + '/assets/' + asset_id + '/short_term_predictions')

        for i in range(0, len(series['date'])):

            test_predictions_firestore_collection.document(series['date'][i]).set({
                'date': str(series['date'][i]),
                'predicted_value': float(series['short_term_prediction'][i])
            })

        print('test_predictions successfully stored in the firestore database')


    def store_short_term_predictions_percentage(self):

        test_predictions_firestore_collection = database.collection('markets/'+ self.market_id + '/assets/' + self.asset_id + '/short_term_predictions_percentage')

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

    
    def store_short_term_prediction(self, market_id, asset_id, change):
        
        asset_document = database.document('markets/'+ market_id + '/assets/' + asset_id)

        asset_document.update({
            'short_term_prediction': change
        })

        print('test_predictions have been written to firebase.')


    def store_value(self, market_id, asset_id, name, value):
        
        asset_document = database.document('markets/'+ market_id + '/assets/' + asset_id)

        asset_document.update({
            name: value
        })

        print(name + ' has been written to firebase.')

        

    def store_short_term_test_predictions(self, market_id, asset_id, series):
        
        test_predictions_firestore_collection = database.collection('markets/'+ market_id + '/assets/' + asset_id + '/short_term_test_predictions')

        for i in range(0, len(series['date'])):
            print(series['date'][i])
            test_predictions_firestore_collection.document(series['date'][i]).set({
                'date': str(series['date'][i]),
                'predicted_value': float(series['short_term_prediction'][i])
            })

        print('test_predictions successfully stored in the firestore database')


    ############
    ## DELETE ##
    ############

    def deleteCollection(self, market_id, asset_id, collection):

        for entry in database.collection('markets/' + market_id + '/assets/' + asset_id + '/' + collection).get():
            
            entry_dict = entry.to_dict()
            database.document('markets/' + market_id + '/assets/' + asset_id + '/' + collection + '/' + entry_dict['date']).delete()

        print(collection + ' collection was successfully deleted.')

    ###########
    ## Tests ##
    ###########

    def check_whether_series_is_up_to_date(self, market_id, symbol):
 
        # date_string = '{date:%Y-%m-%d}'.format(date=datetime.today() - timedelta(days=3))

        date_string = '{date:%Y-%m-%d}'.format(date=datetime.today())

        series_collection = database.collection('markets/' + market_id + '/assets/' + symbol + '/series')
        
        
        result_collection = series_collection.where('date', '==', date_string)


        for result in result_collection.get():
            
            print(symbol)
            # print(result)
            return True

        return False

