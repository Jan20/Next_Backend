import pandas
import urllib.request
import json
from database.database import Database
from test_series.sine_series import Sine_Series
 
class AlphaVantage:

    db = Database()

    def fetch_asset_from_alpha_vantage(self, user_id, asset_id, asset_name, asset_symbol, market_id):

        output_size = 'full' # full or compact
        # output_size = 'compact' # full or compact

        # self.db.deleteCollection(user_id, market_id, asset_id, 'series')


        # print('--------')
        # print(asset_symbol)
        # print('--------')


        # dates, closes = [], []

        # response = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + asset_symbol + '&outputsize=' + output_size + '&apikey=6404')
        # series = json.load(response)

        # dates_keys = series['Time Series (Daily)'].keys()

        # for date_key in dates_keys:

        #     dates.append(date_key)
        #     closes.append(float(series['Time Series (Daily)'][date_key]['4. close']))

        # series = pandas.DataFrame(data={'date': dates, 'close': closes})

        series = Sine_Series().create_series()
        # self.db.store_series_to_firestore(user_id, asset_id, asset_name, asset_symbol, market_id, series)

        print('-------------------------------------')
        print('series')
        print(series)
        print('-------------------------------------')

        return series
