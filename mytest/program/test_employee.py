
import unittest
from employee import Employee


class TestEmployee(unittest.TestCase):

    def test_email(self):
        emp_1 = Employee('Matt', 'Cliff', 50000)
        emp_2 = Employee('mike', 'Smith', 60000)

        self.assertEqual(emp_1.email, 'Matt.Cliff@email.com')
        emp1.first = 'John'

        self.assertEqual(emp_1.email, 'John.Cliff@email.com')

    def test_email(self):
        emp_1 = Employee('Matt', 'Cliff', 50000)
        emp_2 = Employee('mike', 'Smith', 60000)

        self.assertEqual(emp_1.email, 'Matt.Cliff@email.com')
        emp1.first = 'John'

        self.assertEqual(emp_1.email, 'John.Cliff@email.com')


if __name__ == '__main__':
    unittest.main()
