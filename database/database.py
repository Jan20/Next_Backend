
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
            
            database.document('markets/' + market_id + '/assets/' + asset_id + '/' + collection + '/' + entry.to_dict()['date']).delete()

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

