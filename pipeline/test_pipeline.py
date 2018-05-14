import unittest
import pandas
from pandas import DataFrame
import numpy.testing as npt
from pipeline import Pipeline
from test_sets.test_series import Test_Series

class Test_Pipeline(unittest.TestCase):

    def test_get_lagged_series(self):
            
        print('----------------')
        print('     Test 1     ')
        print('----------------')

        dates = [

            '2018-05-11',
            '2018-05-10',
            '2018-05-09',
            '2018-05-08',
            '2018-05-07',
            '2018-05-04',
            '2018-05-03',
            '2018-05-02',
            '2018-05-01',
            '2018-04-30'

        ]

        closes = [

            188.59,
            190.04,
            187.36,  
            186.05,
            185.16,
            183.83,
            176.89,
            176.57,
            169.10,
            165.26

        ]

        test_result = pandas.DataFrame(data={'date': dates, 'close': closes})

        print(test_result)
        print(Pipeline().get_lag_series(Test_Series().get_test_series(), 10))
        
        npt.assert_array_equal(Pipeline().get_lag_series(Test_Series().get_test_series(), 10), test_result)

        print('----------------')
        print('     Test 2     ')
        print('----------------')

        dates = [
        
            '2018-04-27',
            '2018-04-26',
            '2018-04-25',
            '2018-04-24',
            '2018-04-23',
            '2018-04-20',
            '2018-04-19',
            '2018-04-18',
            '2018-04-17',
            '2018-04-16',

        ]

        closes = [

            162.32,  
            164.22,  
            163.65,  
            162.94,  
            165.24,  
            165.72,  
            172.80,  
            177.84,  
            178.24,  
            175.82,  

        ]

        test_result = pandas.DataFrame(data={'date': dates, 'close': closes})

        print(test_result)
        print(Pipeline().get_lag_series(Test_Series().get_test_series(),20))
        
        npt.assert_array_equal(Pipeline().get_lag_series(Test_Series().get_test_series(), 20), test_result)

        

if __name__ == '__main__':
    
    unittest.main()
