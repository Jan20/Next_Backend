import unittest
from math_library import Math_Library
from test_series import Test_Series

class Test_Math_Library(unittest.TestCase):

    def test_percentage_change(self):

        self.assertEqual(Math_Library().percentage_change(100, 110), 10)
        self.assertEqual(Math_Library().percentage_change(100, 50), -50)
        self.assertEqual(Math_Library().percentage_change(100, 30), -70)


    def test_sharpe_ratio(self):
        
        series = Test_Series().get_test_series()
        
        self.assertEqual(Math_Library().sharpe_ratio)

if __name__ == '__main__':

    unittest.main()