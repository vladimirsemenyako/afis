precedence = {'!': 1, '&': 2, '|': 3, '>': 4, '~': 5}


def to_rpn(expression) -> int:
    # Tokenize the expression by handling parentheses and whitespace
    tokens = []
    for token in expression.split():
        if token.isalnum():  # Variables like a, b, c
            tokens.append(token)
        elif token in precedence:
            tokens.append(token)
        elif token.startswith('('):
            tokens.extend(['(', token[1:]] if token[1:] else ['('])
        elif token.endswith(')'):
            tokens.extend([token[:-1], ')'] if token[:-1] else [')'])

    output = []
    stack = []

    for i, token in enumerate(tokens):
        if token in precedence:
            if token == '!' and (i == 0 or tokens[i - 1] in precedence or tokens[i - 1] == '('):
                # If '!' is a unary operator, push it immediately
                stack.append(token)
            else:
                while stack and stack[-1] in precedence and precedence[stack[-1]] <= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            output.append(token)
            if stack and stack[-1] == '!':
                output.append(stack.pop())
    return output + stack[::-1]

# def eval_rpn(tokens: list[str]) -> int:
#     stack = []
#     op = {
#         '&': lambda a, b: True if a and b else False,
#         '!': lambda a: True if a is False else False,
#         '|': lambda a, b: True if a or b else False,
#         '>': lambda a, b: ...,
#         '~': lambda a, b: True if a == b else False,
#     }
#     for token in tokens:
#       if token in op:
#         b = stack.pop()
#         a = stack.pop()
#         stack.append(op[token](a, b))
#       else:
#         stack.append(int(token))
#     return stack.pop()

expression = "( a | b ) ~ ! c & ( d & e )"
print(to_rpn(expression))  # Output: 'a b | c ! & d e & &'


