from alphavantage import AlphaVantage
from database import Database
from datetime import datetime, timedelta
from pandas import pandas


class Run_AlphaVantage:
    
    def fetch_assets(self, market_id):

        alphaVantage = AlphaVantage()
        database = Database()

        assets = database.fetch_assets(market_id)

        print(assets)

        for i in range(0, len(assets)):
            
            existing_series = database.fetch_series(market_id, assets['symbol'][i])

            date_string = '{date:%Y-%m-%d}'.format(date=datetime.today() - timedelta(days=3))

            print(existing_series.loc[existing_series['date'] == date_string])

            if existing_series.loc[existing_series['date'] == date_string].empty:
         
                series = alphaVantage.fetch_series(assets['symbol'][i])
                database.store_series(market_id, assets['symbol'][i], 'series', series)




Run_AlphaVantage().fetch_assets('nasdaq')
