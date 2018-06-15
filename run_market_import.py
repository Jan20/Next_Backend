import json
from pprint import pprint
from database import Database

class Market_Import:

    def import_market(self):

        user_id = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'

        database = Database()
        markets = database.fetch_markets(user_id)

        with open('nasdaq.json') as f:

            data = json.load(f)

            pprint(data['corporations'])

            for i in range(0, len(markets)):

                for j in range(0, len(data['corporations'])):
                    
                    print(data['corporations'][j])
                    print(markets[i])
                    database.store_market(user_id, markets[i], data['corporations'][j]['name'], data['corporations'][j]['symbol'])

Market_Import().import_market()