from alphavantage import AlphaVantage
from database import Database
from pandas import pandas


class Run_AlphaVantage:
    
    def fetch_assets(self, market_id):

        alphaVantage = AlphaVantage()
        database = Database()

        assets = database.fetch_assets(market_id)

        print(assets)

        for i in range(0, len(assets)):
            
            if database.check_whether_series_is_up_to_date(market_id, assets['symbol'][i]) == False:

                series = alphaVantage.fetch_series(assets['symbol'][i])
                database.store_series(market_id, assets['symbol'][i], 'series', series)




Run_AlphaVantage().fetch_assets('nasdaq')
