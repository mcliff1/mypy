import unittest
from mock import patch

from employee import Employee


class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        self.emp_1 = Employee('Matt', 'Cliff', 50000)
        self.emp_2 = Employee('mike', 'Smith', 60000)

    def tearDown(self):
        pass

    def test_email(self):

        self.assertEqual(self.emp_1.email, 'Matt.Cliff@email.com')
        self.emp_1.first = 'John'

        self.assertEqual(self.emp_1.email, 'John.Cliff@email.com')

    def test_raise(self):

        self.assertEqual(self.emp_1.pay, 50000)
        self.emp_1.apply_raise()

        self.assertEqual(self.emp_1.pay, 52500)


    @patch('employee.requests')
    def test_schedule(self, _mock_req):
        _mock_req.get.return_value.ok = True
        _mock_req.get.return_value.text = 'June Schedule for {}'.format(self.emp_1.last)
        self.assertEqual(self.emp_1.schedule('june'), 'June Schedule for Cliff')

if __name__ == '__main__':
    unittest.main()
