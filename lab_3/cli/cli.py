from lab_3.api.api import MinimizationLogic

def print_menu():
    print("\nВыберите метод минимизации:")
    print("1. Минимизировать СКНФ расчетным методом с выводом результата стадии склеивания")
    print("2. Минимизировать СДНФ расчетным методом с выводом результата стадии склеивания")
    print("3. Минимизировать СКНФ расчетно-табличным методом с выводом результата стадии склеивания и таблицы")
    print("4. Минимизировать СДНФ расчетно-табличным методом с выводом результата стадии склеивания и таблицы")
    print("5. Минимизировать СКНФ табличным методом (карта Карно) c выводом таблицы")
    print("6. Минимизировать СДНФ табличным методом (карта Карно) c выводом таблицы")
    print("0. Выход")

def main():
    while True:
        print_menu()
        choice = input("\nВведите номер операции (0-6): ")
        
        if choice == "0":
            print("Программа завершена.")
            break
            
        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Неверный выбор. Пожалуйста, выберите число от 0 до 6.")
            continue
            
        expression = input("\nВведите логическое выражение: ")
        
        try:
            if choice == "1":
                result = MinimizationLogic.minimize_PCNF_calc_method(expression)
                print("\nРезультат минимизации СКНФ расчетным методом:")
                print(result)
                
            elif choice == "2":
                result = MinimizationLogic.minimize_PDNF_calc_method(expression)
                print("\nРезультат минимизации СДНФ расчетным методом:")
                print(result)
                
            elif choice == "3":
                result = MinimizationLogic.minimize_PCNF_table_method(expression)
                print("\nРезультат минимизации СКНФ расчетно-табличным методом:")
                print(result)
                
            elif choice == "4":
                result = MinimizationLogic.minimize_PDNF_table_method(expression)
                print("\nРезультат минимизации СДНФ расчетно-табличным методом:")
                print(result)
                
            elif choice == "5":
                result = MinimizationLogic.minimize_PCNF_karnaugh_method(expression)
                print("\nРезультат минимизации СКНФ методом карт Карно:")
                print(result)
                
            elif choice == "6":
                result = MinimizationLogic.minimize_PDNF_karnaugh_method(expression)
                print("\nРезультат минимизации СДНФ методом карт Карно:")
                print(result)
                
        except Exception as e:
            print(f"\nПроизошла ошибка: {str(e)}")
            
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main() 