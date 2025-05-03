from lab_2.api.api import BooleanLogicAPI
import itertools
from prettytable import PrettyTable


class MinimizationLogic:
    class TermProcessor:
        def __init__(self, variables):
            self.variables = variables
            self.num_vars = len(variables)

        def term_to_binary(self, term, is_pdnf=True):
            """Перевод из логического представления в бинарное"""
            binary = ['0' if is_pdnf else '1'] * self.num_vars
            split_char = '&' if is_pdnf else '|'
            literals = [lit.strip() for lit in term.split(split_char)]

            for lit in literals:
                if lit.startswith('!'):
                    var = lit[1:]
                    idx = self.variables.index(var)
                    binary[idx] = '0' if is_pdnf else '1'
                else:
                    idx = self.variables.index(lit)
                    binary[idx] = '1' if is_pdnf else '0'
            return ''.join(binary)

        def binary_to_term(self, binary, is_pdnf=True):
            """Перевод из бинарного представления в логическое"""
            parts = []
            for i, bit in enumerate(binary):
                if is_pdnf:
                    if bit == '0':
                        parts.append(f'!{self.variables[i]}')
                    elif bit == '1':
                        parts.append(self.variables[i])
                else:
                    if bit == '0':
                        parts.append(self.variables[i])
                    elif bit == '1':
                        parts.append(f'!{self.variables[i]}')
            join_char = ' & ' if is_pdnf else ' | '
            return join_char.join(parts) if parts else ("1" if is_pdnf else "0")

    @staticmethod
    def get_variables(expression):
        """Получение всех переменных из выражения"""
        tokens = BooleanLogicAPI.to_rpn(expression)
        return sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})

    @staticmethod
    def count_differences(t1, t2):

        count = 0
        pos = -1
        for i in range(len(t1)):
            if t1[i] != t2[i]:
                count += 1
                pos = i
        return (count, pos)

    @staticmethod
    def combine_terms(terms, processor, is_pdnf=True):
        new_terms = set()
        used = set()
        operation = '∨' if is_pdnf else '&'

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                t1 = terms[i]
                t2 = terms[j]
                diff_count, diff_pos = MinimizationLogic.count_differences(t1, t2)

                if diff_count == 1:
                    new_term = t1[:diff_pos] + 'X' + t1[diff_pos + 1:]
                    new_terms.add(new_term)
                    used.add(i)
                    used.add(j)
                    print(
                        f"({processor.binary_to_term(t1, is_pdnf)}) {operation} ({processor.binary_to_term(t2, is_pdnf)}) => {processor.binary_to_term(new_term, is_pdnf)}")

        for i in range(len(terms)):
            if i not in used:
                new_terms.add(terms[i])

        return sorted(new_terms)

    @staticmethod
    def check_redundant_terms(final_terms, original_terms, processor, is_pdnf=True):
        """Проверка на лишние импликанты"""
        print("\nПроверка на лишние импликанты:")
        essential_terms = []

        for i, term in enumerate(final_terms):
            covered = []
            for orig_term in original_terms:
                match = True
                for k in range(processor.num_vars):
                    if term[k] != 'X' and term[k] != orig_term[k]:
                        match = False
                        break
                if match:
                    covered.append(orig_term)

            is_essential = False
            for covered_term in covered:
                covered_by_others = False
                for j, other_term in enumerate(final_terms):
                    if j != i:
                        match = True
                        for k in range(processor.num_vars):
                            if other_term[k] != 'X' and other_term[k] != covered_term[k]:
                                match = False
                                break
                        if match:
                            covered_by_others = True
                            break

                if not covered_by_others:
                    is_essential = True
                    break

            if is_essential:
                print(f"{processor.binary_to_term(term, is_pdnf)} - существенная импликанта")
                essential_terms.append(term)
            else:
                print(f"{processor.binary_to_term(term, is_pdnf)} - лишняя импликанта")

        return essential_terms

    @staticmethod
    def minimize_PDNF_calc_method(expression: str) -> str:
        initial_pdnf = BooleanLogicAPI.generate_PDNF(expression)
        if initial_pdnf == "0":
            return "0"

        minterms = [term.strip()[1:-1] for term in initial_pdnf.split("|")]
        variables = MinimizationLogic.get_variables(expression)
        processor = MinimizationLogic.TermProcessor(variables)

        print("Расчетный метод")
        print(f"Исходная СДНФ: {' ∨ '.join(f'({term}){i + 1}' for i, term in enumerate(minterms))}")

        current_terms = [processor.term_to_binary(term) for term in minterms]
        print(f"({', '.join(term for term in current_terms)})")

        print("\nЭтап склеивания 1")
        current_terms = MinimizationLogic.combine_terms(current_terms, processor)
        print("\nРезультат после первого склеивания:")
        print(" ∨ ".join(f"({processor.binary_to_term(term)}){i + 1}" for i, term in enumerate(current_terms)))
        print(f"({', '.join(term.replace('X', '-') for term in current_terms)})")

        minimized = False
        while not minimized:
            new_terms = MinimizationLogic.combine_terms(current_terms, processor)
            if len(new_terms) == len(current_terms):
                minimized = True
            else:
                current_terms = new_terms
                print("\nРезультат после склеивания:")
                print(" ∨ ".join(f"({processor.binary_to_term(term)})" for term in current_terms))
                print(f"({', '.join(term.replace('X', '-') for term in current_terms)})")

        original_minterms = [processor.term_to_binary(term) for term in minterms]
        essential_terms = MinimizationLogic.check_redundant_terms(current_terms, original_minterms, processor)

        if not essential_terms:
            return "0"

        result_terms = sorted(set(processor.binary_to_term(term) for term in essential_terms))
        return " ∨ ".join(f"({term})" for term in result_terms)

    @staticmethod
    def minimize_PCNF_calc_method(expression: str) -> str:
        initial_pcnf = BooleanLogicAPI.generate_PCNF(expression)
        if initial_pcnf == "1":
            return "1"

        maxterms = [term.strip()[1:-1] for term in initial_pcnf.split("&")]
        variables = MinimizationLogic.get_variables(expression)
        processor = MinimizationLogic.TermProcessor(variables)

        print("Расчетный метод для СКНФ")
        print(f"Исходная СКНФ: {' & '.join(f'({term}){i + 1}' for i, term in enumerate(maxterms))}")

        current_terms = [processor.term_to_binary(term, is_pdnf=False) for term in maxterms]
        print(f"({', '.join(term for term in current_terms)})")

        print("\nЭтап склеивания 1")
        current_terms = MinimizationLogic.combine_terms(current_terms, processor, is_pdnf=False)
        print("\nРезультат после первого склеивания:")
        print(" & ".join(
            f"({processor.binary_to_term(term, is_pdnf=False)}){i + 1}" for i, term in enumerate(current_terms)))
        print(f"({', '.join(term.replace('X', '-') for term in current_terms)})")

        minimized = False
        while not minimized:
            new_terms = MinimizationLogic.combine_terms(current_terms, processor, is_pdnf=False)
            if len(new_terms) == len(current_terms):
                minimized = True
            else:
                current_terms = new_terms
                print("\nРезультат после склеивания:")
                print(" & ".join(f"({processor.binary_to_term(term, is_pdnf=False)})" for term in current_terms))
                print(f"({', '.join(term.replace('X', '-') for term in current_terms)})")

        original_maxterms = [processor.term_to_binary(term, is_pdnf=False) for term in maxterms]
        essential_terms = MinimizationLogic.check_redundant_terms(current_terms, original_maxterms, processor,
                                                                  is_pdnf=False)

        if not essential_terms:
            return "1"

        result_terms = sorted(set(processor.binary_to_term(term, is_pdnf=False) for term in essential_terms))
        return " & ".join(f"({term})" for term in result_terms)

    @staticmethod
    def minimize_PDNF_table_method(expression: str) -> str:
        initial_pdnf = BooleanLogicAPI.generate_PDNF(expression)
        if initial_pdnf == "0":
            return "0"

        minterms = [term.strip()[1:-1] for term in initial_pdnf.split("|")]
        variables = MinimizationLogic.get_variables(expression)
        processor = MinimizationLogic.TermProcessor(variables)

        print("Расчетно-табличный метод")
        print(f"Исходная СДНФ: {' ∨ '.join(f'({term}){i + 1}' for i, term in enumerate(minterms))}")

        # Преобразуем термы в бинарный вид
        binary_terms = [processor.term_to_binary(term) for term in minterms]
        original_binary_terms = binary_terms.copy()

        # Этап 1: Склеивание (аналогично расчетному методу)
        minimized = False
        current_terms = binary_terms
        while not minimized:
            new_terms = MinimizationLogic.combine_terms(current_terms, processor)
            if len(new_terms) == len(current_terms):
                minimized = True
            else:
                current_terms = new_terms

        # Этап 2: Построение таблицы покрытия
        print("\nТаблица покрытия:")
        
        # Создаем красивую таблицу
        table = PrettyTable()
        # Заголовки столбцов
        table.field_names = ["Импликанты"] + [f"({term})" for term in minterms]
        
        # Добавляем строки в таблицу
        for imp in current_terms:
            row = [processor.binary_to_term(imp)]
            for orig in original_binary_terms:
                match = True
                for i in range(len(imp)):
                    if imp[i] != 'X' and imp[i] != orig[i]:
                        match = False
                        break
                row.append("X" if match else " ")
            table.add_row(row)
            
        # Выводим таблицу
        print(table)

        # Этап 3: Выделение существенных импликант
        essential_terms = MinimizationLogic.check_redundant_terms(current_terms, original_binary_terms, processor)

        if not essential_terms:
            return "0"

        result_terms = sorted(set(processor.binary_to_term(term) for term in essential_terms))
        return " ∨ ".join(f"({term})" for term in result_terms)

    @staticmethod
    def minimize_PCNF_table_method(expression: str) -> str:
        initial_pcnf = BooleanLogicAPI.generate_PCNF(expression)
        if initial_pcnf == "1":
            return "1"

        maxterms = [term.strip()[1:-1] for term in initial_pcnf.split("&")]
        variables = MinimizationLogic.get_variables(expression)
        processor = MinimizationLogic.TermProcessor(variables)

        print("Расчетно-табличный метод для СКНФ")
        print(f"Исходная СКНФ: {' & '.join(f'({term}){i + 1}' for i, term in enumerate(maxterms))}")

        # Преобразуем термы в бинарный вид
        binary_terms = [processor.term_to_binary(term, is_pdnf=False) for term in maxterms]
        original_binary_terms = binary_terms.copy()

        # Этап 1: Склеивание (аналогично расчетному методу)
        minimized = False
        current_terms = binary_terms
        current_terms = MinimizationLogic.combine_terms(current_terms, processor, is_pdnf=False)
        while not minimized:
            new_terms = MinimizationLogic.combine_terms(current_terms, processor, is_pdnf=False)
            if len(new_terms) == len(current_terms):
                minimized = True
            else:
                current_terms = new_terms

        # Этап 2: Построение таблицы покрытия
        print("\nТаблица покрытия:")
        
        # Создаем красивую таблицу
        table = PrettyTable()
        # Заголовки столбцов
        table.field_names = ["Импликанты"] + [f"({term})" for term in maxterms]
        
        # Добавляем строки в таблицу
        for imp in current_terms:
            row = [processor.binary_to_term(imp, is_pdnf=False)]
            for orig in original_binary_terms:
                match = True
                for i in range(len(imp)):
                    if imp[i] != 'X' and imp[i] != orig[i]:
                        match = False
                        break
                row.append("X" if match else " ")
            table.add_row(row)
            
        # Выводим таблицу
        print(table)

        # Этап 3: Выделение существенных импликант
        essential_terms = MinimizationLogic.check_redundant_terms(current_terms, original_binary_terms, processor, is_pdnf=False)

        if not essential_terms:
            return "1"

        result_terms = sorted(set(processor.binary_to_term(term, is_pdnf=False) for term in essential_terms))
        return " & ".join(f"({term})" for term in result_terms)

    @staticmethod
    def generate_gray_code(n):
        if n == 1:
            return ['0', '1']
        prev_gray_code = MinimizationLogic.generate_gray_code(n - 1)
        gray_code = ['0' + num for num in prev_gray_code] + ['1' + num for num in reversed(prev_gray_code)]
        return gray_code

    @staticmethod
    def create_karnaugh_map(variables, truth_values, minimized_expression=None):
        amount_var = len(variables)
        half = amount_var // 2
        headers = MinimizationLogic.generate_gray_code(amount_var - half)
        side_headers = MinimizationLogic.generate_gray_code(half)
        table = PrettyTable()
        table.field_names = [f'{variables[:half]} \\ {variables[half:]}'] + headers

        for side in side_headers:
            row = [side]
            for col_header in headers:
                gray_index = side + col_header
                value = truth_values.get(gray_index, '')
                row.append(value)
            table.add_row(row)
        print(table)
        return table

    @staticmethod
    def find_groups(variables, truth_values, is_pdnf):
        amount_var = len(variables)
        half = amount_var // 2
        headers = MinimizationLogic.generate_gray_code(amount_var - half)
        side_headers = MinimizationLogic.generate_gray_code(half)

        groups = []

        for side in side_headers:
            for col_header in headers:
                gray_index = side + col_header
                if not is_pdnf and truth_values.get(gray_index, '') == 0:
                    groups.append((side, col_header))
                elif is_pdnf and truth_values.get(gray_index, '') == 1:
                    groups.append((side, col_header))
        return groups

    @staticmethod
    def merge_groups(groups):
        merged = []
        used = set()
        for i in range(len(groups)):
            part1 = groups[i]
            for j in range(i + 1, len(groups)):
                part2 = groups[j]
                if len(part1) != len(part2):
                    continue
                different_var = [(x, y) for x, y in zip(part1, part2) if x != y]
                if len(different_var) == 1 and (
                        (different_var[0][0] == '0' and different_var[0][1] == '1') or
                        (different_var[0][0] == '1' and different_var[0][1] == '0')
                ):
                    differences = [x != y for x, y in zip(part1, part2)]
                    merged_part = [x if not diff else '-' for x, diff in zip(part1, differences)]
                    merged.append(''.join(merged_part))
                    used.add(i)
                    used.add(j)
        for k in range(len(groups)):
            if k not in used:
                merged.append(''.join(groups[k]))

        unique_elements = set()
        final_result = []

        for elem in merged:
            if elem not in unique_elements:
                unique_elements.add(elem)
                final_result.append(elem)

        return final_result

    @staticmethod
    def _check_redundant_terms_silent(final_terms, original_terms, processor, is_pdnf=True):
        """Проверка на лишние импликанты без вывода"""
        essential_terms = []

        for i, term in enumerate(final_terms):
            covered = []
            for orig_term in original_terms:
                match = True
                for k in range(processor.num_vars):
                    if term[k] != 'X' and term[k] != orig_term[k]:
                        match = False
                        break
                if match:
                    covered.append(orig_term)

            is_essential = False
            for covered_term in covered:
                covered_by_others = False
                for j, other_term in enumerate(final_terms):
                    if j != i:
                        match = True
                        for k in range(processor.num_vars):
                            if other_term[k] != 'X' and other_term[k] != covered_term[k]:
                                match = False
                                break
                        if match:
                            covered_by_others = True
                            break

                if not covered_by_others:
                    is_essential = True
                    break

            if is_essential:
                essential_terms.append(term)

        return essential_terms

    @staticmethod
    def _combine_terms_silent(terms, processor, is_pdnf=True):
        new_terms = set()
        used = set()

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                t1 = terms[i]
                t2 = terms[j]
                diff_count, diff_pos = MinimizationLogic.count_differences(t1, t2)

                if diff_count == 1:
                    new_term = t1[:diff_pos] + 'X' + t1[diff_pos + 1:]
                    new_terms.add(new_term)
                    used.add(i)
                    used.add(j)

        for i in range(len(terms)):
            if i not in used:
                new_terms.add(terms[i])

        return sorted(new_terms)

    @staticmethod
    def _minimize_PDNF_calc_method_silent(expression: str) -> str:
        initial_pdnf = BooleanLogicAPI.generate_PDNF(expression)
        if initial_pdnf == "0":
            return "0"

        minterms = [term.strip()[1:-1] for term in initial_pdnf.split("|")]
        variables = MinimizationLogic.get_variables(expression)
        processor = MinimizationLogic.TermProcessor(variables)

        current_terms = [processor.term_to_binary(term) for term in minterms]
        current_terms = MinimizationLogic._combine_terms_silent(current_terms, processor)

        minimized = False
        while not minimized:
            new_terms = MinimizationLogic._combine_terms_silent(current_terms, processor)
            if len(new_terms) == len(current_terms):
                minimized = True
            else:
                current_terms = new_terms

        original_minterms = [processor.term_to_binary(term) for term in minterms]
        essential_terms = MinimizationLogic._check_redundant_terms_silent(current_terms, original_minterms, processor)

        if not essential_terms:
            return "0"

        result_terms = sorted(set(processor.binary_to_term(term) for term in essential_terms))
        return " ∨ ".join(f"({term})" for term in result_terms)

    @staticmethod
    def _minimize_PCNF_calc_method_silent(expression: str) -> str:
        initial_pcnf = BooleanLogicAPI.generate_PCNF(expression)
        if initial_pcnf == "1":
            return "1"

        maxterms = [term.strip()[1:-1] for term in initial_pcnf.split("&")]
        variables = MinimizationLogic.get_variables(expression)
        processor = MinimizationLogic.TermProcessor(variables)

        current_terms = [processor.term_to_binary(term, is_pdnf=False) for term in maxterms]
        current_terms = MinimizationLogic._combine_terms_silent(current_terms, processor, is_pdnf=False)

        minimized = False
        while not minimized:
            new_terms = MinimizationLogic._combine_terms_silent(current_terms, processor, is_pdnf=False)
            if len(new_terms) == len(current_terms):
                minimized = True
            else:
                current_terms = new_terms

        original_maxterms = [processor.term_to_binary(term, is_pdnf=False) for term in maxterms]
        essential_terms = MinimizationLogic._check_redundant_terms_silent(current_terms, original_maxterms, processor,
                                                                          is_pdnf=False)

        if not essential_terms:
            return "1"

        result_terms = sorted(set(processor.binary_to_term(term, is_pdnf=False) for term in essential_terms))
        return " & ".join(f"({term})" for term in result_terms)

    @staticmethod
    def minimize_karnaugh(expression: str, is_pdnf: bool = True) -> str:
        variables = MinimizationLogic.get_variables(expression)
        truth_values = {}

        # Генерируем все возможные комбинации значений переменных
        combinations = list(itertools.product([0, 1], repeat=len(variables)))

        # Заполняем словарь truth_values
        tokens = BooleanLogicAPI.to_rpn(expression)
        for combo in combinations:
            env = dict(zip(variables, combo))
            result, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens, env)
            result = int(result)
            gray_key = ''.join(map(str, combo))
            truth_values[gray_key] = result

        # Получаем минимизированное выражение
        minimized_expression = MinimizationLogic._minimize_PDNF_calc_method_silent(
            expression) if is_pdnf else MinimizationLogic._minimize_PCNF_calc_method_silent(expression)

        # Создаем карту Карно с отображением минимизированной функции
        karnaugh_map = MinimizationLogic.create_karnaugh_map(variables, truth_values, minimized_expression)

        return minimized_expression

    @staticmethod
    def minimize_PDNF_karnaugh_method(expression: str) -> str:
        return MinimizationLogic.minimize_karnaugh(expression, True)

    @staticmethod
    def minimize_PCNF_karnaugh_method(expression: str) -> str:
        return MinimizationLogic.minimize_karnaugh(expression, False)



# !(!a > !b) | c
# ((a > b & (c | (!d))) | e)
# a > b
# (a > (b & (!c)) | d)
