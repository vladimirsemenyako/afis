import unittest
import lab_1.api as api

class MyTestCase(unittest.TestCase):
    def test_positive_binary_conversion(self):
        binary_num = str(api.BinaryNumber(7))
        self.assertEqual(binary_num, '00000111 (7)')

    def test_add_binary(self):
        binary_num_1 = api.BinaryNumber(-7)
        binary_num_2 = api.BinaryNumber(2)
        self.assertEqual(str(binary_num_1 + binary_num_2), '11111011 (-5)')

    def test_multiplication(self):
        binary_num_1 = api.BinaryNumber(-7)
        binary_num_2 = api.BinaryNumber(2)
        self.assertEqual(str(binary_num_1 * binary_num_2), '1111111111110010 (-14)')

    def test_division(self):
        binary_num_1 = api.BinaryNumber(-9)
        binary_num_2 = api.BinaryNumber(3)
        self.assertEqual(str(binary_num_1 / binary_num_2), '11111101.00000')

    def test_init(self):
        binary_num = api.BinaryNumber(True)
        self.assertRaises(ValueError, api.BinaryNumber, binary_num)

    def test_subtract(self):
        binary_num_1 = api.BinaryNumber(-7)
        binary_num_2 = api.BinaryNumber(2)
        self.assertEqual(str(binary_num_1 - binary_num_2), '11110111 (-9)')
if __name__ == '__main__':
    unittest.main()
