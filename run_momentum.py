from alphavantage import AlphaVantage
from database import Database
from momentum import Momentum

#Main Run Thread
class Run_Momentum:
    
    def run(self):

        user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'

        momentum = Momentum()
        database = Database()

        markets = database.fetch_markets(user_id)
        assets = database.fetch_assets(user_id, markets)

        for i in range(0, len(assets)):
            
            print(assets['asset_id'][i])

            series = database.fetch_series(user_id, assets['market_id'][i], assets['asset_id'][i])

            long_term_sharpe_ratio = momentum.calculate_long_term_sharpe_ratio(series)

            database.store_value(user_id, assets['market_id'][i], assets['asset_id'][i], 'longTermSharpeRatio', long_term_sharpe_ratio)

            # sum = 0
            # for j in range(0, len(sharpe_ratio_series)):

            #    sum = sum + sharpe_ratio_series['value'][j]
            
            # sharpe_ratio = sum / len(sharpe_ratio_series)

            # database.store_value(user_id, assets['market_id'][i], assets['asset_id'][i], 'sharpe_ratio', sharpe_ratio)
            

Run_Momentum().run()
