
import pandas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

# Import a custom service account generated at Firebase.com and initialization of the firebase backend
cred = credentials.Certificate('./database/service_account.json')
firebase_admin.initialize_app(cred)
database = firestore.client()

class Market:

    #
    # The following function is used to create a new market document
    # within the markets collection.
    #
    def create_market(self, name, category, market_id):
    
        database.collection('markets').document(market_id).set({'name': name, 'category': category, 'market_id': market_id})

    #
    # Fetches all markets stored within a database and returns
    # the result as an array.
    #
    #
    def fetch_markets(self):

        markets = []

        for market in database.collection('markets').get():
            
            markets.append(str(market.to_dict()['market_id']))

        return markets
