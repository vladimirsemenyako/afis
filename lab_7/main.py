from api import *

def main():
    # Генерируем начальную матрицу
    matrix = generate_matrix()

    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ:")
        print("1. Показать матрицу")
        print("2. Вывести слово по номеру")
        print("3. Перегенерировать матрицу")
        print("4. Ввести слово по номеру")
        print("5. Логические операции над словами")
        print("6. Сложение полей A и B в словах с заданным V")
        print("7. Поиск слов в интервале индексов")
        print("0. Выход")
        print("=" * 50)

        try:
            choice = int(input("Выберите действие: "))

            if choice == 0:
                print("Программа завершена")
                break
            elif choice == 1:
                print_matrix(matrix)
            elif choice == 2:
                word_num = int(input("Введите номер слова (0-15): "))
                get_word(matrix, word_num)
            elif choice == 3:
                regenerate_matrix(matrix)
                print_matrix(matrix)
            elif choice == 4:
                input_word(matrix)
            elif choice == 5:
                logical_operations(matrix)
            elif choice == 6:
                field_addition(matrix)
            elif choice == 7:
                search_in_interval(matrix)
            else:
                print("Ошибка: выберите действие от 0 до 7")

        except ValueError:
            print("Ошибка: введите корректное число")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем")
            break


if __name__ == "__main__":
    main()