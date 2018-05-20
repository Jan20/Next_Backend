import numpy

class Math_Library:

    def percentage_change(self, x, y):

        return ((y - x) / x) * 100

    
    def sharpe_ratio(self, series, i):
        
        excess_return = series['close'][i] - series['close'][i+6]
        standard_deviation = numpy.std(series['close'].head(len(series)))

        return excess_return / standard_deviation

        


  