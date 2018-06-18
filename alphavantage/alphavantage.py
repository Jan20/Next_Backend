import pandas
import urllib.request
import json
import time
from database.database import Database
from test_series.sine_series import Sine_Series

class AlphaVantage:

    database = Database()

    def fetch_series(self, symbol):
        
        time.sleep(2)

        # output_size = 'full' # full or compact
        output_size = 'compact' # full or compact

        print(symbol)
    
        dates, values = [], []

        response = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=' + output_size + '&apikey=6404')
        series = json.load(response)

        if series['Time Series (Daily)'] is not None:
    
            dates_keys = series['Time Series (Daily)'].keys()

            for date_key in dates_keys:

                dates.append(date_key)     
                values.append(float(series['Time Series (Daily)'][date_key]['4. close']))

            return pandas.DataFrame(data={'date': dates, 'value': values})
