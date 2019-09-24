from alphavantage import AlphaVantage
from database import Database
from pandas import pandas

class Run_AlphaVantage:
    
    def fetch_assets(self, market):

        alphaVantage = AlphaVantage()
        database = Database()

        assets = database.fetch_assets(market)

        print(assets)

        # Goes through all assets stored in a market
        for i in range(0, len(assets)):
            
            if database.check_whether_series_is_up_to_date(market, assets['symbol'][i]) == False:

                series = alphaVantage.fetch_series(assets['symbol'][i])
                Series().store_series(market, assets['symbol'][i], 'series', series)




Run_AlphaVantage().fetch_assets('dax')
Run_AlphaVantage().fetch_assets('nasdaq')
