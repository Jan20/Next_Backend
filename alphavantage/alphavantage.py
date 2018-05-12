import pandas
import urllib.request
import json
from database.database import Database
 
class AlphaVantage:

    db = Database()

    def fetchAssetFromAlphaVantage(self, user_id, asset_id, asset_name, asset_symbol, market_id):

        print(asset_symbol)
        output_size = 'full' # full or compact
        # output_size = 'compact' # full or compact

        dates = []
        closes = []
        
        response = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + asset_symbol + '&outputsize=' + output_size + '&apikey=6404')
        series = json.load(response)   

        dates_keys = series['Time Series (Daily)'].keys()

        for date_key in dates_keys:
            
            dates.append(date_key)
            closes.append(float(series['Time Series (Daily)'][date_key]['4. close']))
        
        data = {'date': dates, 'close': closes}

        series = pandas.DataFrame(data=data)

        # print(series)
        
        self.db.store_series_to_firestore(user_id, asset_id, asset_name, asset_symbol, market_id, series)

        # print('test_predictions successfully stored in the firestore database')

        return series
