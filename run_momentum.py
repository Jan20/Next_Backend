from alphavantage import AlphaVantage
from database import Database
from momentum import Momentum

#Main Run Thread
class Run_Momentum:
    
    def run(self):

        momentum = Momentum()
        database = Database()

        markets = database.fetch_markets()
    
        for i in range(0, len(markets)):
    
            assets = database.fetch_assets(markets[i])
        
        for j in range(0, len(assets)):
            
            print(assets['symbol'][j])

            series = database.fetch_series(assets['market_id'][j], assets['symbol'][j])

            long_term_sharpe_ratio = momentum.calculate_long_term_sharpe_ratio(series)

            database.store_value(assets['market_id'][j], assets['symbol'][j], 'longTermSharpeRatio', long_term_sharpe_ratio)

Run_Momentum().run()
