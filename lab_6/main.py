class HashTable:
    def __init__(self, size=20, base_address=0):
        self.size = size
        self.base_address = base_address
        self.table = [None] * size
        self.russian_alphabet = {
            'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ё': 6, 'Ж': 7, 'З': 8, 'И': 9, 'Й': 10,
            'К': 11, 'Л': 12, 'М': 13, 'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18, 'Т': 19, 'У': 20,
            'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Ъ': 27, 'Ы': 28, 'Ь': 29, 'Э': 30,
            'Ю': 31, 'Я': 32
        }
    
    def _calculate_v(self, key):
        """Вычисляет значение V по первым двум буквам ключа (фамилии)"""
        if len(key) < 2:
            raise ValueError("Ключ должен содержать минимум 2 символа")
        
        first_char = key[0].upper()
        second_char = key[1].upper()
        
        if first_char not in self.russian_alphabet or second_char not in self.russian_alphabet:
            raise ValueError("Ключ должен содержать только русские буквы")
        
        v = self.russian_alphabet[first_char] * 33 + self.russian_alphabet[second_char]
        return v
    
    def _hash(self, key):
        """Вычисляет хеш-адрес для ключа"""
        v = self._calculate_v(key)
        return (v % self.size) + self.base_address
    
    def insert(self, key, value):
        """Вставляет пару ключ-значение в хеш-таблицу"""
        index = self._hash(key)
        
        # Квадратичный поиск свободной ячейки
        i = 0
        original_index = index
        while True:
            current_index = (original_index + i * i) % self.size
            if self.table[current_index] is None or self.table[current_index] == 'DELETED':
                self.table[current_index] = (key, value)
                return
            elif self.table[current_index][0] == key:
                # Обновляем существующее значение
                self.table[current_index] = (key, value)
                return
            i += 1
            if i >= self.size:
                raise Exception("Хеш-таблица переполнена")
    
    def search(self, key):
        """Ищет значение по ключу в хеш-таблице"""
        index = self._hash(key)
        
        # Квадратичный поиск
        i = 0
        original_index = index
        while True:
            current_index = (original_index + i * i) % self.size
            if self.table[current_index] is None:
                return None
            elif self.table[current_index] != 'DELETED' and self.table[current_index][0] == key:
                return self.table[current_index][1]
            i += 1
            if i >= self.size:
                return None
    
    def delete(self, key):
        """Удаляет пару ключ-значение из хеш-таблицы"""
        index = self._hash(key)
        
        # Квадратичный поиск
        i = 0
        original_index = index
        while True:
            current_index = (original_index + i * i) % self.size
            if self.table[current_index] is None:
                return False
            elif self.table[current_index] != 'DELETED' and self.table[current_index][0] == key:
                self.table[current_index] = 'DELETED'
                return True
            i += 1
            if i >= self.size:
                return False
    
    def display(self):
        """Выводит содержимое хеш-таблицы"""
        print("Хеш-таблица:")
        print("Индекс | Ключ | Значение")
        print("-----------------------")
        for i in range(self.size):
            if self.table[i] is None:
                print(f"{i:6} | {'':4} | {'':7}")
            elif self.table[i] == 'DELETED':
                print(f"{i:6} | {'DELETED':4} | {'':7}")
            else:
                key, value = self.table[i]
                print(f"{i:6} | {key:4} | {value:7}")


# Пример использования
# if __name__ == "__main__":
#     ht = HashTable()
#
#     # CRUD операции
#     print("Добавляем элементы:")
#     ht.insert("Вяткин", "Студент1")
#     ht.insert("Третьяк", "Студент2")
#     ht.insert("Абрамов", "Студент3")
#     ht.insert("Борисов", "Студент4")
#     ht.display()
#
#     print("\nПоиск элементов:")
#     print("Вяткин:", ht.search("Вяткин"))
#     print("Третьяк:", ht.search("Третьяк"))
#     print("Несуществующий:", ht.search("Несуществующий"))
#
#     print("\nОбновляем элемент:")
#     ht.insert("Вяткин", "Обновленный студент")
#     print("Вяткин после обновления:", ht.search("Вяткин"))
#
#     print("\nУдаляем элемент:")
#     ht.delete("Третьяк")
#     ht.display()
#
#     print("\nПопытка поиска удаленного элемента:")
#     print("Третьяк:", ht.search("Третьяк"))