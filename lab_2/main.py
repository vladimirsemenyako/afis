from cli import BooleanLogicCLI

if __name__ == '__main__':
    expr = "( a | b ) & ! c"
    BooleanLogicCLI.display_all(expr, logic_expr_col_width=20)