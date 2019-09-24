import pandas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

# Import a custom service account generated at Firebase.com and initialization of the firebase backend
cred = credentials.Certificate('./database/service_account.json')
firebase_admin.initialize_app(cred)
database = firestore.client()

class Assets:

    #
    # Creates a new asset and expects a name, a corresponding
    # symbol and a market_id of the market the new asset should
    # belong to.
    #
    def create_asset(self, name, symbol, market_id):
            
        database.collection('markets/'+ market_id + '/assets').document(symbol).set({'name': name, 'symbol': symbol, 'market_id': market_id})

    #
    # Returns all assets currently stored in a market collection.
    #
    #
    #
    def fetch_assets(self, market_id):

        dataframe = pandas.DataFrame(columns=['name', 'symbol', 'market_id'])

        for asset in database.collection('markets/' + market_id + '/assets').get():
            
            dataframe = dataframe.append({'name': asset_dict['name'], 'symbol': asset_dict['symbol'], 'market_id': asset.to_dict()['market_id']}, ignore_index=True)

        return dataframe

    #
    #
    #
    #
    #
    #
    def update_asset(self, market_id, asset_id, value_name, value):
        
        database.document('markets/'+ market_id + '/assets/' + asset_id).update({
        
            value_name: value
        
        })

        print('an existing asset has been updated.')
        