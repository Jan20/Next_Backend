
import pandas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

# Import a custom service account generated at Firebase.com and initialization of the firebase backend
cred = credentials.Certificate('./database/service_account.json')
firebase_admin.initialize_app(cred)
database = firestore.client()

class Series:
    
    #
    # 
    #
    #
    def fetch_series(self, market, symbol):
        
        dataframe = pandas.DataFrame(columns=['date', 'value'])

        for series in database.collection('markets/' + market + '/assets/' + symbol + '/series').get():
            
            dataframe = dataframe.append({'date': series.to_dict()['date'], 'value': series.to_dict()['value']}, ignore_index=True)

        return dataframe

    #
    #
    #
    #
    #
    #
    def store_series(self, market_id, symbol, series_name, series):
        
        firestore_collection = database.collection('markets/'+ market_id + '/assets/' + symbol + '/' + series_name)

        dataframe = pandas.DataFrame(columns=['date', 'value'])

        for entry in firestore_collection.get():

            dataframe = dataframe.append({'date': entry.to_dict()['date'], 'value': entry.to_dict()['value']}, ignore_index=True)

        dataframe = series[(~series.date.isin(dataframe.date))]

        if (len(dataframe['date']) > 1):
            
            for i in range(0, len(dataframe['date'])):

                print(str(dataframe['date'][i]))

                firestore_collection.document(dataframe['date'][i]).set({
                
                    'date': str(dataframe['date'][i]),
                    'value': float(dataframe['value'][i])
            
                })

            print('Series has been saved at Firestore.')