from main import HashTable
import unittest


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=10)  # Используем меньший размер для тестирования коллизий

    def test_insert_and_search(self):
        """Тест вставки и поиска элементов"""
        self.ht.insert("Вяткин", "Студент1")
        self.ht.insert("Третьяк", "Студент2")

        # Проверка поиска существующих элементов
        self.assertEqual(self.ht.search("Вяткин"), "Студент1")
        self.assertEqual(self.ht.search("Третьяк"), "Студент2")

        # Проверка поиска несуществующего элемента
        self.assertIsNone(self.ht.search("Несуществующий"))

    def test_insert_collision(self):
        """Тест обработки коллизий при вставке"""
        # Подберем ключи, которые дадут одинаковый хеш для теста коллизий
        # Для размера таблицы 10: hash("АА") = (0*33 + 0) % 10 = 0
        # hash("КК") = (11*33 + 11) % 10 = (363 + 11) % 10 = 374 % 10 = 4
        # hash("ББ") = (1*33 + 1) % 10 = 34 % 10 = 4 - коллизия с "КК"

        self.ht.insert("КК", "Значение1")
        self.ht.insert("ББ", "Значение2")  # Должно вызвать коллизию

        self.assertEqual(self.ht.search("КК"), "Значение1")
        self.assertEqual(self.ht.search("ББ"), "Значение2")

    def test_update_value(self):
        """Тест обновления значения"""
        self.ht.insert("Вяткин", "Старое значение")
        self.assertEqual(self.ht.search("Вяткин"), "Старое значение")

        self.ht.insert("Вяткин", "Новое значение")
        self.assertEqual(self.ht.search("Вяткин"), "Новое значение")

    def test_delete(self):
        """Тест удаления элементов"""
        self.ht.insert("Вяткин", "Студент1")
        self.assertTrue(self.ht.delete("Вяткин"))
        self.assertIsNone(self.ht.search("Вяткин"))

        # Попытка удалить несуществующий элемент
        self.assertFalse(self.ht.delete("Несуществующий"))

    def test_delete_collision(self):
        """Тест удаления при наличии коллизий"""
        self.ht.insert("КК", "Значение1")
        self.ht.insert("ББ", "Значение2")  # Коллизия

        self.assertTrue(self.ht.delete("ББ"))
        self.assertIsNone(self.ht.search("ББ"))
        self.assertEqual(self.ht.search("КК"), "Значение1")  # Другой элемент должен остаться

    def test_invalid_key(self):
        """Тест обработки некорректных ключей"""
        with self.assertRaises(ValueError):
            self.ht.insert("A", "Латинская буква")  # Не русская

        with self.assertRaises(ValueError):
            self.ht.insert("Я", "Одна буква")  # Слишком короткий

    def test_display(self):
        """Тест отображения таблицы (визуальная проверка)"""
        self.ht.insert("Вяткин", "Студент1")
        self.ht.insert("Третьяк", "Студент2")
        print("\nВизуальная проверка отображения:")
        self.ht.display()


if __name__ == "__main__":
    unittest.main()