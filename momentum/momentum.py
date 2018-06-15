import numpy
import pandas
import matplotlib.pyplot as plt
from math_library.math_library import Math_Library 
from database import Database

class Momentum:

    def calculate_long_term_sharpe_ratio(self, series):

        print(series)
        sharpe_ratio = Math_Library().sharpe_ratio(series)

        print(sharpe_ratio)

        return sharpe_ratio

        # dates = []
        # values = []
        # i = 0

        # while i < len(series):

        #     if ((i + 6) > len(series)):

        #         break
            
            
        #     short_series = series.iloc[i:i+7]
        #     print(short_series)
        #     sharpe_ratio = Math_Library().sharpe_ratio(short_series, i)

        #     dates.append(series['date'][i])
        #     values.append(sharpe_ratio)
        #     print(i)
        #     print(sharpe_ratio) 

        #     i = i + 7


        # temp = pandas.DataFrame(data={'date':dates, 'value':values})

        # print(temp)

        # plt.plot(temp['value'], label='Value')
        # plt.legend()
        # plt.show()

        # return temp
        
