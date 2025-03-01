import itertools

class BooleanLogicAPI:

    precedence = {'!': 1, '&': 2, '|': 3, '>': 4, '~': 5}

    @staticmethod
    def to_rpn(expression: str):
        tokens = []
        for token in expression.split():
            while token.startswith('('):
                tokens.append('(')
                token = token[1:]
            while token.endswith(')'):
                if token[:-1]:
                    tokens.append(token[:-1])
                tokens.append(')')
                token = ''
            if token:
                tokens.append(token)
        output = []
        stack = []
        for i, token in enumerate(tokens):
            if token.isalnum():
                output.append(token)
                if stack and stack[-1] == '!':
                    output.append(stack.pop())
            elif token in BooleanLogicAPI.precedence:
                if token == '!' and (i == 0 or tokens[i-1] in BooleanLogicAPI.precedence or tokens[i-1] == '('):
                    stack.append(token)
                else:
                    while (stack and stack[-1] in BooleanLogicAPI.precedence and
                           BooleanLogicAPI.precedence[stack[-1]] <= BooleanLogicAPI.precedence[token]):
                        output.append(stack.pop())
                    stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack:
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
        binary_string = "".join(bits)
        decimal_value = int(binary_string, 2)
        return f"{decimal_value} - {binary_string}"
