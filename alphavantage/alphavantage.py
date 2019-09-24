import pandas
import urllib.request
import json
import time
from database.database import Database
from test_series.sine_series import Sine_Series

class AlphaVantage:

    database = Database()

    def fetch_series(self, symbol):
        
        time.sleep(5)   

        output_size = 'compact' # full or compact

        dates, values = [], []
        dataframe = pandas.DataFrame(columns=['date', 'value'])

        response = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=' + output_size + '&apikey=6404')
        series = json.load(response)

        if series['Time Series (Daily)'] is not None:
    
            for date_key in series['Time Series (Daily)'].keys():

                dates.append(date_key)     
                values.append(float(series['Time Series (Daily)'][date_key]['4. close']))

            return dataframe
