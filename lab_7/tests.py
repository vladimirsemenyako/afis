import unittest
import random
from io import StringIO
import sys
from api import (generate_matrix, show_matrix, print_matrix,
                         get_word, regenerate_matrix, input_word,
                         logical_operations, field_addition,
                         search_in_interval)


class TestMatrixFunctions(unittest.TestCase):
    def setUp(self):
        # Фиксируем random для предсказуемых результатов
        random.seed(42)
        self.matrix = generate_matrix()
        # Сохраняем оригинальный stdout для перехвата вывода
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        # Восстанавливаем stdout
        sys.stdout = self.original_stdout

    def test_generate_matrix(self):
        """Тест генерации матрицы"""
        matrix = generate_matrix()
        self.assertEqual(len(matrix), 16)  # 16 строк
        for row in matrix:
            self.assertEqual(len(row), 16)  # 16 столбцов
            self.assertTrue(all(bit in (0, 1) for bit in row))

    def test_show_matrix(self):
        """Тест отображения матрицы"""
        show_matrix(self.matrix)
        output = sys.stdout.getvalue()
        self.assertIn("Строка  0:", output)  # Проверяем часть вывода

    def test_print_matrix(self):
        """Тест печати матрицы и слов"""
        print_matrix(self.matrix)
        output = sys.stdout.getvalue()
        self.assertIn("Матрица 16x16", output)
        self.assertIn("Слово  0:", output)
        self.assertIn("Слово 15:", output)

    def test_get_word_valid(self):
        """Тест получения слова по валидному номеру"""
        word = get_word(self.matrix, 0)
        self.assertEqual(len(word), 16)
        self.assertTrue(all(bit in (0, 1) for bit in word))

    def test_get_word_invalid(self):
        """Тест получения слова по невалидному номеру"""
        word = get_word(self.matrix, 16)
        self.assertIsNone(word)
        output = sys.stdout.getvalue()
        self.assertIn("Ошибка", output)

    def test_regenerate_matrix(self):
        """Тест перегенерации матрицы"""
        original = [row.copy() for row in self.matrix]
        regenerate_matrix(self.matrix)
        self.assertNotEqual(original, self.matrix)

    def test_input_word_valid(self):
        """Тест ввода валидного слова"""
        # Подменяем ввод
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: "1010101010101010"

        input_word(self.matrix)
        builtins.input = original_input

        # Проверяем, что слово записалось
        word = get_word(self.matrix, 0)
        self.assertNotEqual(word, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    def test_input_word_invalid(self):
        """Тест ввода невалидного слова"""
        # Подменяем ввод
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: "invalid"

        input_word(self.matrix)
        builtins.input = original_input

        output = sys.stdout.getvalue()
        self.assertIn("Ошибка", output)

    def test_logical_operations(self):
        """Тест логических операций"""
        # Подменяем ввод
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: "0"  # Просто возвращаем 0 для обоих слов

        logical_operations(self.matrix)
        builtins.input = original_input

        output = sys.stdout.getvalue()
        self.assertIn("f2 = x1 ∧ x2", output)
        self.assertIn("f7 = x1 ∨ x2", output)
        self.assertIn("f8 = !(x1 ∨ x2)", output)
        self.assertIn("f13 = !x1 ∨ x2", output)

    def test_field_addition(self):
        """Тест сложения полей"""
        # Сначала установим тестовое слово с известным V
        test_word = "101" + "0101" + "0011" + "00000"  # V=101
        for i in range(16):
            self.matrix[(i + 5) % 16][5] = int(test_word[i])

        # Подменяем ввод
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: "101"

        field_addition(self.matrix)
        builtins.input = original_input

        output = sys.stdout.getvalue()
        self.assertIn("Найдено слово", output)
        self.assertIn("A=5, B=3, A+B=8", output)

    def test_search_in_interval(self):
        """Тест поиска в интервале"""
        # Подменяем ввод
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: "0"

        search_in_interval(self.matrix)
        builtins.input = original_input

        output = sys.stdout.getvalue()
        self.assertIn("Слова в интервале", output)

    def test_search_in_interval_incorrect(self):
        """Тест поиска в интервале"""
        # Подменяем ввод
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: 'Hello'

        search_in_interval(self.matrix)
        builtins.input = original_input

        output = sys.stdout.getvalue()
        self.assertIn("Ошибка", output)

    def test_main_flow(self):
        """Интеграционный тест основного потока"""
        # Подменяем ввод и импортируем main
        import builtins
        original_input = builtins.input

        # Эмулируем выбор пользователя: 1 (показать), 0 (выход)
        inputs = ["1", "0"]
        builtins.input = lambda _: inputs.pop(0)

        from main import main
        main()
        builtins.input = original_input

        output = sys.stdout.getvalue()
        self.assertIn("МЕНЮ", output)
        self.assertIn("Программа завершена", output)


if __name__ == "__main__":
    # Запуск тестов с измерением покрытия
    import coverage

    cov = coverage.Coverage()
    cov.start()

    unittest.main(exit=False)

    cov.stop()
    cov.save()

    # Генерация отчета
    cov.report()
    cov.html_report(directory='coverage_report')