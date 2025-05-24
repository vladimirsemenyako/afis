import random


def generate_matrix():
    """Генерирует матрицу 16x16 со случайными 0 и 1, где слова - это столбцы со смещением"""
    matrix = [[0 for _ in range(16)] for _ in range(16)]
    for i in range(16):
        for j in range(16):
            # Каждое следующее слово (столбец) смещено на 1 бит
            matrix[(i + j) % 16][j] = random.randint(0, 1)
    return matrix


def show_matrix(matrix):
    """Выводит матрицу в виде таблицы"""
    print("Матрица 16x16 (слова - столбцы со смещением):")
    for i in range(16):
        print(f"Строка {i:2d}:", end=' ')
        for j in range(16):
            print(matrix[i][j], end=' ')
        print()


def print_matrix(matrix):
    """Выводит матрицу и слова (столбцы) в удобном формате"""
    show_matrix(matrix)
    print("\nСлова (столбцы со смещением):")
    for word_num in range(16):
        word = [matrix[(i + word_num) % 16][word_num] for i in range(16)]
        print(f"Слово {word_num:2d}: {''.join(map(str, word))}")


def get_word(matrix, word_num):
    """Функция 1: Вывести слово по его номеру (от 0 до 15)"""
    if 0 <= word_num <= 15:
        word = [matrix[(i + word_num) % 16][word_num] for i in range(16)]
        print(f"Слово {word_num}: {''.join(map(str, word))}")
        return word
    else:
        print("Ошибка: номер слова должен быть от 0 до 15")
        return None


def regenerate_matrix(matrix):
    """Функция 2: Перегенерировать матрицу"""
    for i in range(16):
        for j in range(16):
            matrix[i][j] = random.randint(0, 1)
    print("Матрица перегенерирована!")


def input_word(matrix):
    """Функция 3: Ввести слово по его номеру"""
    try:
        word_input = input("Введите 16 символов (0 или 1): ")
        if len(word_input) != 16 or not all(c in '01' for c in word_input):
            print("Ошибка: нужно ввести ровно 16 символов, состоящих из 0 и 1")
            return

        position = int(input("Введите позицию для размещения (0-15): "))
        if not (0 <= position <= 15):
            print("Ошибка: позиция должна быть от 0 до 15")
            return

        # Записываем слово в столбец с соответствующим смещением
        for i in range(16):
            matrix[(i + position) % 16][position] = int(word_input[i])
        print(f"Слово размещено в позиции {position}")

    except ValueError:
        print("Ошибка: некорректный ввод")


def logical_operations(matrix):
    """Функция 4: Провести логические выражения над словами"""
    try:
        num1 = int(input("Введите номер первого слова (0-15): "))
        num2 = int(input("Введите номер второго слова (0-15): "))

        if not (0 <= num1 <= 15 and 0 <= num2 <= 15):
            print("Ошибка: номера слов должны быть от 0 до 15")
            return

        word1 = [matrix[(i + num1) % 16][num1] for i in range(16)]
        word2 = [matrix[(i + num2) % 16][num2] for i in range(16)]

        print(f"\nСлово {num1}: {''.join(map(str, word1))}")
        print(f"Слово {num2}: {''.join(map(str, word2))}")
        print("\nРезультаты логических операций:")

        # f2 = x1 ∧ x2 (AND)
        f2 = [word1[i] & word2[i] for i in range(16)]
        print(f"f2 = x1 ∧ x2: {''.join(map(str, f2))}")

        # f7 = x1 ∨ x2 (OR)
        f7 = [word1[i] | word2[i] for i in range(16)]
        print(f"f7 = x1 ∨ x2: {''.join(map(str, f7))}")

        # f8 = !(x1 ∨ x2) (NOR)
        f8 = [1 - (word1[i] | word2[i]) for i in range(16)]
        print(f"f8 = !(x1 ∨ x2): {''.join(map(str, f8))}")

        # f13 = !x1 ∨ x2 (IMPLICATION)
        f13 = [(1 - word1[i]) | word2[i] for i in range(16)]
        print(f"f13 = !x1 ∨ x2: {''.join(map(str, f13))}")

    except ValueError:
        print("Ошибка: некорректный ввод")


def field_addition(matrix):
    """Функция 5: Сложение полей Aj Bj в словах Sj, у которых Vj совпадает с заданным V"""
    try:
        v_input = input("Введите V (3 бита, например 101): ")
        if len(v_input) != 3 or not all(c in '01' for c in v_input):
            print("Ошибка: V должно содержать ровно 3 бита (0 или 1)")
            return

        target_v = v_input
        print(f"\nИщем слова с V = {target_v}")

        modified_count = 0
        for word_num in range(16):
            # Получаем слово как столбец со смещением
            word = [matrix[(i + word_num) % 16][word_num] for i in range(16)]
            word_str = ''.join(map(str, word))

            # Разделение слова: V(3) A(4) B(4) S(5)
            v = word_str[0:3]
            a = word_str[3:7]
            b = word_str[7:11]
            s = word_str[11:16]

            if v == target_v:
                print(f"\nНайдено слово {word_num}: {word_str}")
                print(f"  V={v}, A={a}, B={b}, S={s}")

                # Преобразуем A и B в числа и складываем
                a_val = int(a, 2)
                b_val = int(b, 2)
                sum_val = a_val + b_val

                # Преобразуем сумму обратно в 5-битное представление
                new_s = format(sum_val, '05b')[-5:]  # Берем последние 5 бит

                print(f"  A={a_val}, B={b_val}, A+B={sum_val}")
                print(f"  Новый S: {s} -> {new_s}")

                # Обновляем слово в матрице
                new_word_str = v + a + b + new_s
                for i in range(16):
                    matrix[(i + word_num) % 16][word_num] = int(new_word_str[i])

                modified_count += 1

        if modified_count == 0:
            print(f"Слова с V = {target_v} не найдены")
        else:
            print(f"\nИзменено слов: {modified_count}")

    except ValueError:
        print("Ошибка: некорректный ввод")


def search_in_interval(matrix):
    """Функция 6: Поиск величин, заключенных в данном интервале"""
    try:
        start = int(input("Введите начальный индекс интервала (0-15): "))
        end = int(input("Введите конечный индекс интервала (0-15): "))

        if not (0 <= start <= 15 and 0 <= end <= 15):
            print("Ошибка: индексы должны быть от 0 до 15")
            return

        print(f"\nСлова в интервале от {start} до {end}:")
        for word_num in range(start, end + 1):
            word = [matrix[(i + word_num) % 16][word_num] for i in range(16)]
            print(f"Слово {word_num}: {''.join(map(str, word))}")

    except ValueError:
        print("Ошибка: некорректный ввод")
