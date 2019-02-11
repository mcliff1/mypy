import unittest
from mock import patch
from program.data import write_out

class TestProgram(unittest.TestCase):
    """
    to run this use nosetests in the parent directory
    """

    @patch('cPickle.dump')
    @patch('__builtin__.open', spec=file)
    def test_write_out(self, mock_open, mock_pickle):
        path = '~/testpath'
        f = mock_open.return_value.__enter__.return_value
        f.method.return_value = path

        write_out(path, 'data')

        mock_open.assert_called_once_with(path, 'wb')
        mock_pickle.assert_called_once_with('data', f)



if __name__ == '__main__':
    unittest.main()
