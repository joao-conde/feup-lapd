import unittest
from stuns.utils import sum


class TestUtils(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum(3, 4), 7)