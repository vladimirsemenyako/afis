import sys
import io
import unittest
from unittest.mock import patch
from lab_1.cli import BinaryCLI

class TestBinaryCLI(unittest.TestCase):
    def run_cli_with_inputs(self, inputs):
        """
        Вспомогательный метод для запуска CLI с заданной последовательностью вводимых данных.
        Возвращает захваченный вывод (stdout) в виде строки.
        """
        input_iter = iter(inputs)
        with patch('builtins.input', side_effect=lambda prompt="": next(input_iter)):
            with patch('sys.stdout', new_callable=io.StringIO) as fake_stdout:
                # Ожидаем завершения работы через sys.exit()
                with self.assertRaises(SystemExit):
                    cli = BinaryCLI()
                    cli.run()
                return fake_stdout.getvalue()

    def test_addition_binary(self):
        output = self.run_cli_with_inputs(["1", "5", "3", "6"])
        self.assertIn("Результат (бинарное): 00001000 (8)", output)

    def test_ieee754_addition(self):
        output = self.run_cli_with_inputs(["2", "2.0", "3.0", "6"])
        self.assertIn("Результат (IEEE‑754): IEEE-754: 01000000101000000000000000000000 | Float: 5.0", output)

    def test_substract_binary(self):
        output = self.run_cli_with_inputs(["3", "5", "3", "6"])
        self.assertIn('Результат: 00000010 (2)', output)

    def test_multiplication_binary(self):
        output = self.run_cli_with_inputs(["4", "15", "4", "6"])
        self.assertIn("Результат: 0000000000111100 (60)", output)

    def test_division_binary(self):
        output = self.run_cli_with_inputs(["5", "15", "4", "6"])
        self.assertIn('Результат (бинарный): 00000011.11000', output)

    def test_division_by_zero(self):
        output = self.run_cli_with_inputs(["5", "15", "0", "6"])
        self.assertIn('Ошибка: деление на ноль невозможно.', output)

    def test_float_sign(self):
        output = self.run_cli_with_inputs(["2", "-2.0", "3.0", "6"])
        self.assertIn('Только положительные числа поддерживаются!', output)
if __name__ == '__main__':
    unittest.main()
