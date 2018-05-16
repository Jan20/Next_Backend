import matplotlib.pyplot as plt
import numpy as numpy
import pandas
from pandas import DataFrame
import datetime

class Sine_Series:

    def create_series(self):
        
        Fs = 2000
        f = 5
        sample = 2000
        x = numpy.arange(sample)
        print
        y = numpy.sin(2 * numpy.pi * f * x / Fs)
        plt.plot(x, y)
        plt.xlabel('sample(n)')
        plt.ylabel('voltage(V)')
        # plt.show()

        dates = []
        for i in range(0, 2000):
            dates.append(str(datetime.date.today() - datetime.timedelta(days=i)))

        z = pandas.DataFrame(data={'date': dates, 'close': y})
        print(z)
        # plt.show(z)
        return z

Sine_Series().create_series()













