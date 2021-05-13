import unittest

from cut_finder import CutFinder


class MainTests(unittest.TestCase):
    def test_basic(self):
        cf = CutFinder(finals=[50, 49], stocks=[100])
        self.assertEqual(cf.finals.used_boards, [50, 49])
        self.assertEqual(cf.finals.unused_boards, list())
        self.assertEqual(cf.stocks.unused_boards, list())

    def test_largest_remainder(self):
        cf = CutFinder(finals=[50], stocks=[100, 200])
        self.assertEqual(cf.finals.used_boards, [50])
        self.assertEqual(cf.finals.unused_boards, list())
        self.assertEqual(cf.stocks.used_boards, [100])
        self.assertEqual(cf.stocks.unused_boards, [200])
        # using the 100 stock leaves the 200, i.e. a larger remainder

    def test_prioritizes_least_waste(self):
        cf = CutFinder(finals=[50, 49, 23], stocks=[100])
        self.assertEqual(cf.finals.unused_boards, [23])
        self.assertEqual(cf.finals.used_boards, [50, 49])
        self.assertEqual(cf.stocks.unused_boards, list())
        # [50, 49] leaves less waste than [50, 23] or [49, 23]

    def test_final_longer_than_stock(self):
        cf = CutFinder(finals=[100], stocks=[99])
        self.assertEqual(cf.finals.unused_boards, [100])
        self.assertEqual(cf.finals.used_boards, list())
        self.assertEqual(cf.stocks.unused_boards, [99])
        self.assertEqual(cf.stocks.used_boards, list())
        # nothing is possible here



if __name__ == '__main__':
    unittest.main()
