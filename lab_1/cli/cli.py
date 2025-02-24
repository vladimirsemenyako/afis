import sys
from lab_1.api import BinaryNumber, IEEE754Float

class BinaryCLI:
    def __init__(self):
        self.operations = {
            '1': ('Сложение (бинарное)', self.addition_binary),
            '2': ('Сложение (IEEE‑754)', self.addition_ieee),
            '3': ('Вычитание', self.subtraction),
            '4': ('Умножение', self.multiplication),
            '5': ('Деление', self.division),
            '6': ('Выход', self.exit_program)
        }

    def run(self):
        while True:
            self.display_menu()
            choice = input("Выберите операцию: ")
            if choice in self.operations:
                self.operations[choice][1]()
            else:
                print("Некорректный выбор. Попробуйте снова.")

    def display_menu(self):
        print("\nВыберите операцию:")
        for key, (name, _) in self.operations.items():
            print(f"{key}. {name}")

    def get_input_numbers(self):
        try:
            num1 = int(input("Введите первое число (целое): "))
            num2 = int(input("Введите второе число (целое): "))
            return BinaryNumber(num1), BinaryNumber(num2)
        except ValueError:
            print("Ошибка ввода! Введите целые числа.")
            return None, None

    def get_input_floats(self):
        try:
            num1 = float(input("Введите первое число (положительный float): "))
            num2 = float(input("Введите второе число (положительный float): "))
            if num1 < 0 or num2 < 0:
                print("Только положительные числа поддерживаются!")
                return None, None
            return IEEE754Float(num1), IEEE754Float(num2)
        except ValueError:
            print("Ошибка ввода! Введите числа с плавающей точкой.")
            return None, None

    def addition_binary(self):
        num1, num2 = self.get_input_numbers()
        if num1 and num2:
            result = num1 + num2
            print(f"Результат (бинарное): {result}")

    def addition_ieee(self):
        num1, num2 = self.get_input_floats()
        if num1 and num2:
            result = num1 + num2
            print(f"Результат (IEEE‑754): {result}")

    def subtraction(self):
        num1, num2 = self.get_input_numbers()
        if num1 and num2:
            result = num1 - num2
            print(f"Результат: {result}")

    def multiplication(self):
        num1, num2 = self.get_input_numbers()
        if num1 and num2:
            result = num1 * num2
            print(f"Результат: {result}")

    def division(self):
        num1, num2 = self.get_input_numbers()
        if num1 and num2:
            try:
                binary_result = num1 / num2  # строка с бинарным представлением (целая часть и дробь)
                decimal_result = num1.to_int() / num2.to_int()
                print(f"Результат (бинарный): {binary_result}")
                print(f"Результат (десятичный): {decimal_result:.5f}")
            except ZeroDivisionError:
                print("Ошибка: деление на ноль невозможно.")

    def exit_program(self):
        print("Выход из программы.")
        sys.exit()

if __name__ == "__main__":
    cli = BinaryCLI()
    cli.run()
