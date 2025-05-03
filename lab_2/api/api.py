import itertools
import re

class BooleanLogicAPI:
    # Higher numbers mean higher precedence.
    precedence = {'!': 5, '&': 4, '|': 3, '>': 2, '~': 1}
    associativity = {'!': 'right', '&': 'left', '|': 'left', '>': 'right', '~': 'left'}

    @staticmethod
    def tokenize(expression: str):
        # This regex matches any operator, parenthesis, or alphanumeric token.
        tokens = re.findall(r'([!&|>~()]|\w+)', expression)
        return tokens

    @staticmethod
    def to_rpn(expression: str):
        tokens = BooleanLogicAPI.tokenize(expression)
        output = []
        stack = []
        for token in tokens:
            if token.isalnum():
                output.append(token)
            elif token in BooleanLogicAPI.precedence:
                while (stack and stack[-1] in BooleanLogicAPI.precedence and
                       ((BooleanLogicAPI.associativity[token] == 'left' and
                         BooleanLogicAPI.precedence[stack[-1]] >= BooleanLogicAPI.precedence[token]) or
                        (BooleanLogicAPI.associativity[token] == 'right' and
                         BooleanLogicAPI.precedence[stack[-1]] > BooleanLogicAPI.precedence[token]))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
        while stack:
            output.append(stack.pop())
        return output

    @staticmethod
    def eval_rpn_with_log(tokens, var_values):
        stack = []
        log = []
        for token in tokens:
            if token in {'!', '&', '|', '>', '~'}:
                if token == '!':
                    operand_val, operand_expr = stack.pop()
                    result_val = not operand_val
                    result_expr = f"!{operand_expr}"
                    stack.append((result_val, result_expr))
                    log.append((result_expr, result_val))
                else:
                    right_val, right_expr = stack.pop()
                    left_val, left_expr = stack.pop()
                    def fmt(expr):
                        if any(op in expr for op in [' ', '&', '|', '>', '~']):
                            if not (expr.startswith('(') and expr.endswith(')')):
                                return f"({expr})"
                        return expr
                    left_formatted = fmt(left_expr)
                    right_formatted = fmt(right_expr)
                    if token == '&':
                        result_val = left_val and right_val
                    elif token == '|':
                        result_val = left_val or right_val
                    elif token == '>':
                        result_val = (not left_val) or right_val
                    elif token == '~':
                        result_val = (left_val == right_val)
                    result_expr = f"{left_formatted} {token} {right_formatted}"
                    stack.append((result_val, result_expr))
                    log.append((result_expr, result_val))
            else:
                if token.isdigit():
                    val = bool(int(token))
                    stack.append((val, token))
                else:
                    val = var_values[token]
                    stack.append((val, token))
        final_val, final_expr = stack.pop()
        return final_val, log, final_expr

    @staticmethod
    def generate_PDNF(expression: str) -> str:
        tokens = BooleanLogicAPI.to_rpn(expression)
        variables = sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})
        minterms = []
        for values in itertools.product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            final_val, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens, assignment)
            if final_val:
                literals = [var if assignment[var] else f"!{var}" for var in variables]
                minterm = "(" + " & ".join(literals) + ")"
                minterms.append(minterm)
        return "0" if not minterms else " | ".join(minterms)

    @staticmethod
    def generate_PCNF(expression: str) -> str:
        tokens = BooleanLogicAPI.to_rpn(expression)
        variables = sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})
        maxterms = []
        for values in itertools.product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            final_val, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens, assignment)
            if not final_val:
                literals = [f"!{var}" if assignment[var] else var for var in variables]
                maxterm = "(" + " | ".join(literals) + ")"
                maxterms.append(maxterm)
        return "1" if not maxterms else " & ".join(maxterms)

    @staticmethod
    def generate_numerical_forms(expression: str) -> str:
        tokens = BooleanLogicAPI.to_rpn(expression)
        variables = sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})
        n = len(variables)
        true_indices = []
        false_indices = []
        for values in itertools.product([False, True], repeat=n):
            index = sum((1 << (n - i - 1)) for i, val in enumerate(values) if val)
            assignment = dict(zip(variables, values))
            final_val, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens, assignment)
            if final_val:
                true_indices.append(index)
            else:
                false_indices.append(index)
        false_indices.sort()
        true_indices.sort()
        pcnf_numerical = "(" + ", ".join(str(i) for i in false_indices) + ") ∧"
        pdnf_numerical = "(" + ", ".join(str(i) for i in true_indices) + ") ∨"
        return pcnf_numerical + "\n" + pdnf_numerical

    @staticmethod
    def generate_indexing_form(expression: str) -> str:
        tokens = BooleanLogicAPI.to_rpn(expression)
        variables = sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})
        n = len(variables)
        bits = []
        for values in itertools.product([False, True], repeat=n):
            assignment = dict(zip(variables, values))
            final_val, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens, assignment)
            bits.append("1" if final_val else "0")
        binary_string = " ".join(bits)
        decimal_value = int("".join(bits), 2)
        return f"{decimal_value} - {binary_string}"

    @staticmethod
    def are_equivalent(expr1: str, expr2: str) -> bool:
        """
        Проверяет, являются ли два булевых выражения эквивалентными.
        """
        tokens1 = BooleanLogicAPI.to_rpn(expr1)
        tokens2 = BooleanLogicAPI.to_rpn(expr2)
        
        # Получаем все переменные из обоих выражений
        variables1 = {token for token in tokens1 if token.isalpha() and token not in BooleanLogicAPI.precedence}
        variables2 = {token for token in tokens2 if token.isalpha() and token not in BooleanLogicAPI.precedence}
        all_variables = sorted(variables1.union(variables2))
        
        # Проверяем все возможные комбинации значений переменных
        for values in itertools.product([False, True], repeat=len(all_variables)):
            assignment = dict(zip(all_variables, values))
            val1, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens1, assignment)
            val2, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens2, assignment)
            if val1 != val2:
                return False
        return True

    @staticmethod
    def is_tautology(expression: str) -> bool:
        """
        Проверяет, является ли выражение тавтологией.
        """
        tokens = BooleanLogicAPI.to_rpn(expression)
        variables = sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})
        
        for values in itertools.product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            val, _, _ = BooleanLogicAPI.eval_rpn_with_log(tokens, assignment)
            if not val:
                return False
        return True

    @staticmethod
    def minimize_PDNF(expression: str) -> str:
        # First generate the initial PDNF
        initial_pdnf = BooleanLogicAPI.generate_PDNF(expression)
        if initial_pdnf == "0":
            return "0"

        # Parse the initial PDNF into minterms
        minterms = [term.strip()[1:-1] for term in initial_pdnf.split("|")]

        # Get all variables from the expression
        tokens = BooleanLogicAPI.to_rpn(expression)
        variables = sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})
        num_vars = len(variables)

        print("Расчетный метод")
        print(f"Исходная СДНФ: {' ∨ '.join(f'({term}){i + 1}' for i, term in enumerate(minterms))}")

        # Convert minterms to binary representation (X is don't care)
        def term_to_binary(term):
            binary = ['0'] * num_vars
            literals = [lit.strip() for lit in term.split('&')]
            for lit in literals:
                if lit.startswith('!'):
                    var = lit[1:]
                    idx = variables.index(var)
                    binary[idx] = '0'
                else:
                    idx = variables.index(lit)
                    binary[idx] = '1'
            return ''.join(binary)

        # Convert binary back to term
        def binary_to_term(binary):
            parts = []
            for i, bit in enumerate(binary):
                if bit == '0':
                    parts.append(f'!{variables[i]}')
                elif bit == '1':
                    parts.append(variables[i])
                # X (don't care) is omitted
            return ' & '.join(parts) if parts else "1"

        # Convert term to binary with X for missing variables
        def term_to_binary_x(term):
            binary = ['X'] * num_vars
            literals = [lit.strip() for lit in term.split('&')]
            for lit in literals:
                if lit.startswith('!'):
                    var = lit[1:]
                    idx = variables.index(var)
                    binary[idx] = '0'
                else:
                    idx = variables.index(lit)
                    binary[idx] = '1'
            return ''.join(binary)

        # Step 1: Initial minterms
        current_terms = [term_to_binary(term) for term in minterms]
        print(f"({', '.join(term for term in current_terms)})")

        # Function to count differences between two terms
        def count_differences(t1, t2):
            count = 0
            pos = -1
            for i in range(num_vars):
                if t1[i] != t2[i]:
                    count += 1
                    pos = i
            return (count, pos)

        # Step 2: First stage of combining
        print("\nЭтап склеивания 1")
        new_terms = set()
        used = set()

        for i in range(len(current_terms)):
            for j in range(i + 1, len(current_terms)):
                t1 = current_terms[i]
                t2 = current_terms[j]
                diff_count, diff_pos = count_differences(t1, t2)

                if diff_count == 1:
                    new_term = t1[:diff_pos] + 'X' + t1[diff_pos + 1:]
                    new_terms.add(new_term)
                    used.add(i)
                    used.add(j)
                    print(f"({binary_to_term(t1)}) ∨ ({binary_to_term(t2)}) => {binary_to_term(new_term)}")

        # Add terms that couldn't be combined
        for i in range(len(current_terms)):
            if i not in used:
                new_terms.add(current_terms[i])

        current_terms = sorted(new_terms)
        print("\nРезультат после первого склеивания:")
        print(" ∨ ".join(f"({binary_to_term(term)}){i + 1}" for i, term in enumerate(current_terms)))
        print(f"({', '.join(term.replace('X', '-') for term in current_terms)})")

        # Step 3: Second stage of combining if possible
        minimized = False
        while not minimized:
            new_terms = set()
            used = set()
            term_list = list(current_terms)

            for i in range(len(term_list)):
                for j in range(i + 1, len(term_list)):
                    t1 = term_list[i]
                    t2 = term_list[j]
                    diff_count, diff_pos = count_differences(t1, t2)

                    if diff_count == 1:
                        new_term = t1[:diff_pos] + 'X' + t1[diff_pos + 1:]
                        new_terms.add(new_term)
                        used.add(i)
                        used.add(j)
                        print(f"({binary_to_term(t1)}) ∨ ({binary_to_term(t2)}) => {binary_to_term(new_term)}")

            # Add terms that couldn't be combined
            for i in range(len(term_list)):
                if i not in used:
                    new_terms.add(term_list[i])

            if len(new_terms) == len(current_terms):
                minimized = True
            else:
                current_terms = sorted(new_terms)
                print("\nРезультат после склеивания:")
                print(" ∨ ".join(f"({binary_to_term(term)})" for term in current_terms))
                print(f"({', '.join(term.replace('X', '-') for term in current_terms)})")

        # Step 4: Check for redundant implicants
        print("\nПроверка на лишние импликанты:")
        final_terms = current_terms.copy()
        essential_terms = []

        # Convert original minterms to binary
        original_minterms = [term_to_binary(term) for term in minterms]

        for i, term in enumerate(final_terms):
            # Find all original minterms covered by this term
            covered = []
            for minterm in original_minterms:
                match = True
                for k in range(num_vars):
                    if term[k] != 'X' and term[k] != minterm[k]:
                        match = False
                        break
                if match:
                    covered.append(minterm)

            # Check if any minterm is only covered by this term
            is_essential = False
            for minterm in covered:
                covered_by_others = False
                for j, other_term in enumerate(final_terms):
                    if j != i:
                        match = True
                        for k in range(num_vars):
                            if other_term[k] != 'X' and other_term[k] != minterm[k]:
                                match = False
                                break
                        if match:
                            covered_by_others = True
                            break

                if not covered_by_others:
                    is_essential = True
                    break

            if is_essential:
                print(f"{binary_to_term(term)} - существенная импликанта")
                essential_terms.append(term)
            else:
                print(f"{binary_to_term(term)} - лишняя импликанта")

        # Create final result
        if not essential_terms:
            return "0"

        result_terms = sorted(set(binary_to_term(term) for term in essential_terms))
        return " ∨ ".join(f"({term})" for term in result_terms)
# Пример использования:
# expr = "!(!a > !b) | c"
# print("Исходная СДНФ:", BooleanLogicAPI.generate_PDNF(expr))
# print("Минимизированная СДНФ:", BooleanLogicAPI.minimize_PDNF(expr))
# # Example usage:
# expression = "!( a | b ) > ! c"
# result = BooleanLogicAPI.generate_indexing_form(expression)
# print("Минимизированная СДНФ:", BooleanLogicAPI.minimize_PDNF(expression))
# print(result)
