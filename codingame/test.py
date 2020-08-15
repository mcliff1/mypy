import unittest

from codingame.surface import Surface


class TestSurface(unittest.TestCase):
    def test_init(self):
        """ tests some creations """
        data = [[0,0], [10,10], [20,0]]
        surface = Surface(data)
        self.assertTrue(surface)
        print(f'surface: {surface}')


        print(f'pairs: {surface.pairs}')
        #surface.find_lz()


        hits = surface.detect_collision((0, 10), (20, 0)) # should hit
        print(f'hits: {hits}')


if __name__ == '__main__':
    unittest.main()
