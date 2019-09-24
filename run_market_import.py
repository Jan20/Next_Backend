import json
from pprint import pprint
from database import Database

class Market_Import:

    ###############
    ## Variables ##
    ###############

    database = Database()
    markets = database.fetch_markets()


    def create_market(self, name, category, market_id):
        
        self.database.create_market(name, category, market_id)


    def import_market(self, market_id, json_path):

        with open(json_path) as nasdaq:

            data = json.load(nasdaq)

            pprint(data['corporations'])

            for i in range(0, len(data['corporations'])):
                
                print(data['corporations'][i])
                self.database.create_asset(data['corporations'][i]['name'], data['corporations'][i]['symbol'], market_id)

market_import = Market_Import()

market_import.create_market('Nasdaq', 'American Tech Index', 'nasdaq')
market_import.import_market('nasdaq', 'import/nasdaq.json')

market_import.create_market('DAX', 'German 30 Index', 'dax')
market_import.import_market('dax', 'import/dax.json')