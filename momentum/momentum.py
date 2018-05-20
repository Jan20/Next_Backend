import numpy
import pandas
import matplotlib.pyplot as plt
from math_library.math_library import Math_Library 


class Momentum:

    def create_prediction(self, series):

        dates = []
        values = []
        i = 0

        while i < len(series):

            if ((i + 6) > len(series)):

                break
            
            
            short_series = series.iloc[i:i+7]
            print(short_series)
            sharpe_ratio = Math_Library().sharpe_ratio(short_series, i)

            dates.append(series['date'][i])
            values.append(sharpe_ratio)
            print(i)
            print(sharpe_ratio) 

            i = i + 6


        temp = pandas.DataFrame(data={'date':dates, 'value':values})
        print(temp)

        plt.plot(temp['value'], label='Value')
        plt.legend()
        plt.show()

        return temp
        
