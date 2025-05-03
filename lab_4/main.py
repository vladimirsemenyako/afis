from lab_2.api.api import BooleanLogicAPI
from lab_3.api.api import MinimizationLogic

# Первая таблица (ODS_3_truth_table)
# Столбцы P и S
ODS_3_truth_table = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [0, 1, 1, 1, 0],
    [1, 0, 1, 1, 0],
    [1, 1, 1, 1, 1]
]

# Вторая таблица (D8421_plus_4_truth_table)
# Столбцы 5,6,7,8
D8421_plus_4_truth_table = [
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 1],
    [0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 1]
]

def build_sknf_for_ods3():
    """Строит СКНФ для первой таблицы"""
    # Для P (4-й столбец)
    p_terms = []
    for row in ODS_3_truth_table:
        if row[3] == 0:  # P = 0
            a = "!a" if row[0] == 1 else "a"
            b = "!b" if row[1] == 1 else "b"
            c = "!c" if row[2] == 1 else "c"
            p_terms.append(f"({a} | {b} | {c})")
    
    # Для S (5-й столбец)
    s_terms = []
    for row in ODS_3_truth_table:
        if row[4] == 0:  # S = 0
            a = "!a" if row[0] == 1 else "a"
            b = "!b" if row[1] == 1 else "b"
            c = "!c" if row[2] == 1 else "c"
            s_terms.append(f"({a} | {b} | {c})")
    
    return " & ".join(p_terms), " & ".join(s_terms)

def build_sknf_for_d8421():
    """Строит СКНФ для второй таблицы"""
    sknf_5 = []
    sknf_6 = []
    sknf_7 = []
    sknf_8 = []
    
    for row in D8421_plus_4_truth_table:
        a = "!a" if row[0] == 1 else "a"
        b = "!b" if row[1] == 1 else "b"
        c = "!c" if row[2] == 1 else "c"
        d = "!d" if row[3] == 1 else "d"
        
        if row[4] == 0:  # 5-й столбец
            sknf_5.append(f"({a} | {b} | {c} | {d})")
        if row[5] == 0:  # 6-й столбец
            sknf_6.append(f"({a} | {b} | {c} | {d})")
        if row[6] == 0:  # 7-й столбец
            sknf_7.append(f"({a} | {b} | {c} | {d})")
        if row[7] == 0:  # 8-й столбец
            sknf_8.append(f"({a} | {b} | {c} | {d})")
    
    return " & ".join(sknf_5), " & ".join(sknf_6), " & ".join(sknf_7), " & ".join(sknf_8)

def main():
    print("СКНФ для первой таблицы (ODS_3_truth_table):")
    p_sknf, s_sknf = build_sknf_for_ods3()
    print("Исходная СКНФ для P:", p_sknf)
    minimized_p_sknf = MinimizationLogic._minimize_PCNF_calc_method_silent(p_sknf)
    print("Минимизированная СКНФ для P:", minimized_p_sknf)
    
    print("\nИсходная СКНФ для S:", s_sknf)
    minimized_s_sknf = MinimizationLogic._minimize_PCNF_calc_method_silent(s_sknf)
    print("Минимизированная СКНФ для S:", minimized_s_sknf)
    
    print("\nСКНФ для второй таблицы (D8421_plus_4_truth_table):")
    sknf_5, sknf_6, sknf_7, sknf_8 = build_sknf_for_d8421()
    
    print("Исходная СКНФ для 5-го столбца:", sknf_5)
    minimized_sknf_5 = MinimizationLogic._minimize_PCNF_calc_method_silent(sknf_5)
    print("Минимизированная СКНФ для 5-го столбца:", minimized_sknf_5)
    
    print("\nИсходная СКНФ для 6-го столбца:", sknf_6)
    minimized_sknf_6 = MinimizationLogic._minimize_PCNF_calc_method_silent(sknf_6)
    print("Минимизированная СКНФ для 6-го столбца:", minimized_sknf_6)
    
    print("\nИсходная СКНФ для 7-го столбца:", sknf_7)
    minimized_sknf_7 = MinimizationLogic._minimize_PCNF_calc_method_silent(sknf_7)
    print("Минимизированная СКНФ для 7-го столбца:", minimized_sknf_7)
    
    print("\nИсходная СКНФ для 8-го столбца:", sknf_8)
    minimized_sknf_8 = MinimizationLogic._minimize_PCNF_calc_method_silent(sknf_8)
    print("Минимизированная СКНФ для 8-го столбца:", minimized_sknf_8)

if __name__ == "__main__":
    main() 