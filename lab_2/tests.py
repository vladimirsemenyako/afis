import unittest
import sys
import io
from lab_2.api import BooleanLogicAPI
from lab_2.cli import BooleanLogicCLI
class TestBooleanLogicFunctions(unittest.TestCase):

    def setUp(self):
        self.expr = "( a | b ) & ! c & ( d & e )"
        self.rpn_expected = ["a", "b", "|", "c", "!", "&", "d", "e", "&", "&"]
        self.variables = ['a', 'b', 'c', 'd', 'e']

    def test_to_rpn(self):
        rpn = BooleanLogicAPI.to_rpn(self.expr)
        self.assertEqual(rpn, self.rpn_expected)

    def test_eval_rpn_with_log(self):
        tokens = BooleanLogicAPI.to_rpn(self.expr)
        assignment = {'a': True, 'b': False, 'c': False, 'd': True, 'e': True}
        final_val, log, final_expr = BooleanLogicAPI.eval_rpn_with_log(tokens, assignment)
        self.assertTrue(final_val)
        self.assertTrue(any("!c" in step for step, val in log))

    def test_generate_PDNF(self):
        pdnf = BooleanLogicAPI.generate_PDNF(self.expr)
        expected = "(!a & b & !c & d & e) | (a & !b & !c & d & e) | (a & b & !c & d & e)"
        self.assertEqual(pdnf, expected)

    def test_generate_PCNF(self):
        pcnf = BooleanLogicAPI.generate_PCNF(self.expr)
        # The expression is not a tautology so PCNF should not be "1"
        self.assertNotEqual(pcnf, "1")
        self.assertIn(" & ", pcnf)
        self.assertIn(" | ", pcnf)

    def test_generate_numerical_forms(self):
        num_forms = BooleanLogicAPI.generate_numerical_forms(self.expr)
        # Expected true indices (minterms) for our expression are 11, 19, 27.
        expected_true = "(11, 19, 27) ∨"
        # Expected false indices: all indices in range(32) except 11, 19, 27.
        false_indices = [i for i in range(32) if i not in [11, 19, 27]]
        expected_false = "(" + ", ".join(str(i) for i in false_indices) + ") ∧"
        expected = expected_false + "\n" + expected_true
        self.assertEqual(num_forms, expected)

    def test_generate_indexing_form(self):
        indexing = BooleanLogicAPI.generate_indexing_form(self.expr)
        # For a 5-variable expression there are 32 rows.
        # The expected binary string is constructed based on the evaluation order.
        expected_binary = ("0" * 11) + "1" + ("0" * 7) + "1" + ("0" * 7) + "1" + ("0" * 4)
        expected_indexing = f"{int(expected_binary, 2)} - {expected_binary}"
        self.assertEqual(indexing, expected_indexing)

    def test_numeric_constants(self):
        expr = "1 & ! 0"
        tokens = BooleanLogicAPI.to_rpn(expr)
        self.assertEqual(tokens, ["1", "0", "!", "&"])
        final_val, log, final_expr = BooleanLogicAPI.eval_rpn_with_log(tokens, {})
        self.assertTrue(final_val)

if __name__ == '__main__':
    unittest.main()