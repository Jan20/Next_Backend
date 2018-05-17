import datetime
import pandas

class Linear_Series:

    def create_series(self):

        closes = []
        for i in range(0, 2000):
            
            closes.append(i*4)

        dates = []
        for i in range(0, 2000):
            
            dates.append(str(datetime.date.today() - datetime.timedelta(days=i)))

        df = pandas.DataFrame(data={'date': dates, 'close': closes})

        return df
        