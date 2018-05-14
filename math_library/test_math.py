import unittest
from math_library import Math

class TestMath(unittest.TestCase):

    def test_percentage_change(self):

        self.assertEqual(Math().percentage_change(100, 110), 10)
        self.assertEqual(Math().percentage_change(100, 50), -50)
        self.assertEqual(Math().percentage_change(100, 30), -70)


if __name__ == '__main__':

    unittest.main()