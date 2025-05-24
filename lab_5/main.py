from lab_3.api.api import MinimizationLogic

state_transition_table = [
    [0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 1],
    [0, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1]
]

def build_sknf_for_state_table():
    """Строит СКНФ для 4-го, 5-го и 6-го столбцов таблицы переходов"""
    sknf_4 = []
    sknf_5 = []
    sknf_6 = []
    
    for row in state_transition_table:
        a = "!a" if row[0] == 1 else "a"
        b = "!b" if row[1] == 1 else "b"
        c = "!c" if row[2] == 1 else "c"
        
        if row[3] == 0:  # 4-й столбец
            sknf_4.append(f"({a} | {b} | {c})")
        if row[4] == 0:  # 5-й столбец
            sknf_5.append(f"({a} | {b} | {c})")
        if row[5] == 0:  # 6-й столбец
            sknf_6.append(f"({a} | {b} | {c})")
    
    return " & ".join(sknf_4), " & ".join(sknf_5), " & ".join(sknf_6)

def main():
    print("СКНФ для таблицы переходов:")
    sknf_4, sknf_5, sknf_6 = build_sknf_for_state_table()
    
    print("Исходная СКНФ для 4-го столбца:", sknf_4)
    minimized_sknf_4 = MinimizationLogic._minimize_PCNF_calc_method_silent(sknf_4)
    print("Минимизированная СКНФ для 4-го столбца:", minimized_sknf_4)
    
    print("\nИсходная СКНФ для 5-го столбца:", sknf_5)
    minimized_sknf_5 = MinimizationLogic._minimize_PCNF_calc_method_silent(sknf_5)
    print("Минимизированная СКНФ для 5-го столбца:", minimized_sknf_5)
    
    print("\nИсходная СКНФ для 6-го столбца:", sknf_6)
    print("Минимизированная СКНФ для 6-го столбца:", 1)

if __name__ == "__main__":
    main()

