import datetime
import pandas

class Linear_Series:

    def create_series(self):

        values = []
        for i in range(0, 1000):
            
            values.append(i*4)

        dates = []
        for i in range(0, 1000):
            
            dates.append(str(datetime.date.today() - datetime.timedelta(days=i)))

        dates = []
        for i in range(0, 1000):
            
            dates.append(i)

        df = pandas.DataFrame(data={'date': dates, 'value': values})

        return df
        