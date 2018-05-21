user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'
from alphavantage import AlphaVantage
from database import Database
from momentum import Momentum

#Main Run Thread
class Run_Momentum:
    
    def run(self):

        user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'

        alphaVantage = AlphaVantage()
        momentum = Momentum()
        database = Database()

        markets = database.fetch_markets(user_id)
        assets = database.fetch_assets(user_id, markets)


        for i in range(80, len(assets)):
            
            database.deleteCollection(user_id, assets['market_id'][i], assets['asset_id'][i], 'sharpe_ratio_series')

            series = alphaVantage.fetch_asset(user_id, assets['market_id'][i], assets['asset_id'][i], assets['asset_symbol'][i])

            sharpe_ratio_series = momentum.create_prediction(series)

            database.store_series(user_id, assets['market_id'][i], assets['asset_id'][i], 'sharpe_ratio_series', sharpe_ratio_series)

            sum = 0
            for j in range(0, len(sharpe_ratio_series)):

               sum = sum + sharpe_ratio_series['value'][j]
            
            sharpe_ratio = sum / len(sharpe_ratio_series)

            database.store_value(user_id, assets['market_id'][i], assets['asset_id'][i], 'sharpe_ratio', sharpe_ratio)
            

Run_Momentum().run()
