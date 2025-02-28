import itertools
from lab_2.api import BooleanLogicAPI

class BooleanLogicCLI:
    """
    CLI class for displaying Boolean logic outputs.
    Provides a method for generating a formatted truth table and for printing all results.
    """
    @staticmethod
    def generate_truth_table(expression: str, logic_expr_col_width: int = None) -> str:
        tokens = BooleanLogicAPI.to_rpn(expression)
        variables = sorted({token for token in tokens if token.isalpha() and token not in BooleanLogicAPI.precedence})
        # Create header using a dummy assignment.
        dummy_assignment = {var: False for var in variables}
        _, sample_log, sample_final_expr = BooleanLogicAPI.eval_rpn_with_log(tokens, dummy_assignment)
        headers = variables + [subexpr for subexpr, _ in sample_log] + [sample_final_expr]

        table = [headers]
        for values in itertools.product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            final_val, log_entries, _ = BooleanLogicAPI.eval_rpn_with_log(tokens, assignment)
            row = [ "1" if assignment[var] else "0" for var in variables ]
            row += [ "1" if val else "0" for _, val in log_entries ]
            row.append("1" if final_val else "0")
            table.append(row)

        num_cols = len(table[0])
        col_widths = []
        for i in range(num_cols):
            if i < len(variables):
                max_width = max(len(row[i]) for row in table)
            else:
                max_width = logic_expr_col_width if logic_expr_col_width is not None else max(len(row[i]) for row in table)
            col_widths.append(max_width)

        formatted_rows = []
        for row in table:
            formatted_cells = []
            for i, cell in enumerate(row):
                if i >= len(variables) and logic_expr_col_width is not None:
                    cell = cell[:logic_expr_col_width].ljust(logic_expr_col_width)
                else:
                    cell = cell.ljust(col_widths[i])
                formatted_cells.append(cell)
            formatted_rows.append(" | ".join(formatted_cells))
        separator = "-+-".join("-" * col_widths[i] for i in range(num_cols))
        return formatted_rows[0] + "\n" + separator + "\n" + "\n".join(formatted_rows[1:])

    @staticmethod
    def display_all(expression: str, logic_expr_col_width: int = None) -> None:
        print("RPN:", BooleanLogicAPI.to_rpn(expression))
        print("\nTruth Table:")
        print(BooleanLogicCLI.generate_truth_table(expression, logic_expr_col_width))
        print("\nPDNF:")
        print(BooleanLogicAPI.generate_PDNF(expression))
        print("\nPCNF:")
        print(BooleanLogicAPI.generate_PCNF(expression))
        print("\nNumerical Forms:")
        print(BooleanLogicAPI.generate_numerical_forms(expression))
        print("\nIndexing Form:")
        print(BooleanLogicAPI.generate_indexing_form(expression))

