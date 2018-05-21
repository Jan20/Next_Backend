import matplotlib.pyplot as plt
import numpy as numpy
import pandas
from pandas import DataFrame
import datetime

class Sine_Series:

    def create_series(self):
        
        Fs = 1000
        f = 5
        sample = 1000
        x = numpy.arange(sample)
        print
        y = numpy.sin(2 * numpy.pi * f * x / Fs)
        # plt.plot(x, y)
        # plt.xlabel('sample(n)')
        # plt.ylabel('voltage(V)')
        # plt.show()

        dates = []
        for i in range(0, 1000):
            dates.append(str(datetime.date.today() - datetime.timedelta(days=i)))

        dates = []
        for i in range(-500,500):
            dates.append(i / 500)

        df = pandas.DataFrame(data={'date': dates, 'value': y})
        # print(df)
        # plt.show(z)
        return df














