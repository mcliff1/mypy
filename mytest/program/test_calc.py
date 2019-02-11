import unittest
import calc

class TestCalc(unittest.TestCase):

    def test_add(self):
        self.assertEquals(calc.add(10, 5), 15)

    def test_subtract(self):
        self.assertEquals(calc.subtract(10, 5), 5)

    def test_divide(self):
        self.assertRaises(ValueError, calc.divide, 10, 0)

        # or using cm
        with self.assertRaises(ValueError):
            calc.divide(10, 0)



if __name__ == '__main__':
    unittest.main()


