from alphavantage import AlphaVantage
from database import Database

class Run_AlphaVantage:
    
    def run(self):

        user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'

        alphaVantage = AlphaVantage()
        database = Database()

        markets = database.fetch_markets(user_id)
        assets = database.fetch_assets(user_id, markets)

        for i in range(0, len(assets)):
            
            series = alphaVantage.fetch_asset(user_id, assets['market_id'][i], assets['asset_id'][i], assets['asset_symbol'][i])

            database.store_series(user_id, assets['market_id'][i], assets['asset_id'][i], 'series', series)

Run_AlphaVantage().run()
