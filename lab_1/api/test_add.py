import unittest
import utils


class MyTests(unittest.TestCase):
    def test_add_bin(self):
        x = utils.add_bin("2", "5")
        self.assertEqual(x, "111")

    def test_binary_to_decimal(self):
        x = utils.binary_to_decimal("1010")
        self.assertEqual(x, 10)

    def test_to_bin_sign_mode(self):
        x = utils.to_bin_sign_mode(-10)
        self.assertEqual(x, "1 1010")

    def test_to_bin_ones_complement(self):
        x = utils.to_bin_ones_complement(-10)
        self.assertEqual(x, "1 0101")

    def test_to_bin_twos_complement(self):
        x = utils.to_bin_twos_complement(-10)
        self.assertEqual(x, "1 0110")
if __name__ == '__main__':
    unittest.main()
