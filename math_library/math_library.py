import numpy

class Math_Library:

    def percentage_change(self, x, y):

        return ((y - x) / x) * 100

    
    def sharpe_ratio(self, series):
        
        excess_return = series['value'][len(series)-1] - series['value'][0]
        standard_deviation = numpy.std(series['value'].head(len(series)))

        result = 0

        if (standard_deviation != 0):
            
            result = excess_return / standard_deviation

        return result

        


  