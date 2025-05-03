import unittest
from lab_3.api.api import MinimizationLogic


class TestMinimizationLogic(unittest.TestCase):
    def setUp(self):
        self.test_expressions = {
            'simple': 'a & b',
            'medium': '(a & b) | c',
            'complex': '((a > b) & (c | (!d))) | e',
            'with_implication': 'a > b',
            'with_negation': '!(a & b)',
            'all_operations': '(a & b) | (c > d) & !e'
        }

    def test_get_variables(self):
        # Тест извлечения переменных
        expression = self.test_expressions['complex']
        variables = MinimizationLogic.get_variables(expression)
        self.assertEqual(set(variables), {'a', 'b', 'c', 'd', 'e'})

        # Тест с простым выражением
        expression = self.test_expressions['simple']
        variables = MinimizationLogic.get_variables(expression)
        self.assertEqual(set(variables), {'a', 'b'})

    def test_term_processor(self):
        variables = ['a', 'b', 'c']
        processor = MinimizationLogic.TermProcessor(variables)

        # Тест преобразования термов в бинарный вид
        pdnf_term = 'a & !b & c'
        binary = processor.term_to_binary(pdnf_term, is_pdnf=True)
        self.assertEqual(binary, '101')

        pcnf_term = 'a | !b | c'
        binary = processor.term_to_binary(pcnf_term, is_pdnf=False)
        self.assertEqual(binary, '010')

    def test_count_differences(self):
        # Тест подсчета различий между термами
        term1 = '1010'
        term2 = '1110'
        count, pos = MinimizationLogic.count_differences(term1, term2)
        self.assertEqual(count, 1)
        self.assertEqual(pos, 1)

        # Тест с идентичными термами
        term1 = '1010'
        term2 = '1010'
        count, pos = MinimizationLogic.count_differences(term1, term2)
        self.assertEqual(count, 0)
        self.assertEqual(pos, -1)

    def test_combine_terms(self):
        variables = ['a', 'b']
        processor = MinimizationLogic.TermProcessor(variables)
        
        # Тест склеивания термов СДНФ
        terms = ['00', '01', '10']
        result = MinimizationLogic.combine_terms(terms, processor, is_pdnf=True)
        self.assertTrue('0X' in result or 'X0' in result)

        # Тест склеивания термов СКНФ
        terms = ['00', '01', '11']
        result = MinimizationLogic.combine_terms(terms, processor, is_pdnf=False)
        self.assertTrue('0X' in result or 'X1' in result)

    def test_minimize_pdnf_calc_method(self):
        # Тест минимизации СДНФ
        for expr in self.test_expressions.values():
            result = MinimizationLogic.minimize_PDNF_calc_method(expr)
            self.assertIsInstance(result, str)

    def test_minimize_pcnf_calc_method(self):
        # Тест минимизации СКНФ
        for expr in self.test_expressions.values():
            result = MinimizationLogic.minimize_PCNF_calc_method(expr)
            self.assertIsInstance(result, str)

    def test_minimize_pdnf_table_method(self):
        # Тест табличного метода СДНФ
        for expr in self.test_expressions.values():
            result = MinimizationLogic.minimize_PDNF_table_method(expr)
            self.assertIsInstance(result, str)

    def test_minimize_pcnf_table_method(self):
        # Тест табличного метода СКНФ
        for expr in self.test_expressions.values():
            result = MinimizationLogic.minimize_PCNF_table_method(expr)
            self.assertIsInstance(result, str)

    def test_minimize_karnaugh(self):
        # Тест метода карт Карно
        for expr in self.test_expressions.values():
            # Тест СДНФ
            result_pdnf = MinimizationLogic.minimize_karnaugh(expr, is_pdnf=True)
            self.assertIsInstance(result_pdnf, str)
            
            # Тест СКНФ
            result_pcnf = MinimizationLogic.minimize_karnaugh(expr, is_pdnf=False)
            self.assertIsInstance(result_pcnf, str)

    def test_generate_gray_code(self):
        # Тест генерации кода Грея
        # Для n = 1
        code1 = MinimizationLogic.generate_gray_code(1)
        self.assertEqual(code1, ['0', '1'])

        # Для n = 2
        code2 = MinimizationLogic.generate_gray_code(2)
        self.assertEqual(code2, ['00', '01', '11', '10'])

        # Для n = 3
        code3 = MinimizationLogic.generate_gray_code(3)
        self.assertEqual(len(code3), 8)
        self.assertEqual(len(set(code3)), 8)  # Все коды уникальны

    def test_create_karnaugh_map(self):
        # Тест создания карты Карно
        variables = ['a', 'b']
        truth_values = {'00': 0, '01': 1, '10': 1, '11': 0}
        
        # Тест без минимизированного выражения
        table = MinimizationLogic.create_karnaugh_map(variables, truth_values)
        self.assertIsNotNone(table)

        # Тест с минимизированным выражением
        table = MinimizationLogic.create_karnaugh_map(variables, truth_values, "a ^ b")
        self.assertIsNotNone(table)

    def test_find_groups(self):
        # Тест поиска групп в карте Карно
        variables = ['a', 'b']
        truth_values = {'00': 0, '01': 1, '10': 1, '11': 0}
        
        # Тест для СДНФ
        pdnf_groups = MinimizationLogic.find_groups(variables, truth_values, is_pdnf=True)
        self.assertEqual(len(pdnf_groups), 2)  # Должно быть 2 группы для единиц
        
        # Тест для СКНФ
        pcnf_groups = MinimizationLogic.find_groups(variables, truth_values, is_pdnf=False)
        self.assertEqual(len(pcnf_groups), 2)  # Должно быть 2 группы для нулей


if __name__ == '__main__':
    unittest.main() 