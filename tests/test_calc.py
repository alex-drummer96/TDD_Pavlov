from unittest import TestCase, mock
from unittest.mock import patch
import unittest
from calc.calculator import SimpleCalculator

ERROR_MESSAGE = 'Аргументи повинні бути типами int або float'
TEST_CASES_NEGATIVE = [
            [1, 2, "3", 4.5],
            [None, None, None],
            [1, 2, {}]
        ]
NUMBERS = [1, 2, 3, 4, 5]


class SimpleCalculatorTests(TestCase):
    def setUp(self):
        self.calculator = SimpleCalculator()

    def test_check_args_positive(self):

        for args in TEST_CASES_NEGATIVE:
            with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                self.calculator._check_args(*args)

    def test_check_args_negative(self):
        args = [1, 2, 3, 4.5]
        self.assertIsNone(self.calculator._check_args(*args))

    def test_add_positive(self):
        test_cases = [
            ([1, 2, 3.5], 6.5),
            ([0, 0], 0),
            ([-1, -2, -3.5], -6.5)
        ]

        with mock.patch.object(self.calculator, '_check_args') as mock_check_args:
            for args, expected_result in test_cases:
                result = self.calculator.add(*args)
                self.assertEqual(result, expected_result)
                mock_check_args.assert_called_once_with(*args)
                mock_check_args.reset_mock()

    def test_add_negative(self):

        with patch('calc.calculator.SimpleCalculator._check_args') as mock_check_args:
            for args in TEST_CASES_NEGATIVE:
                mock_check_args.side_effect = ValueError(ERROR_MESSAGE)
                with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                    self.calculator.add(*args)
                mock_check_args.assert_called_once_with(*args)
                mock_check_args.reset_mock()

    def test_subtract_positive(self):
        test_cases = [
            (10, 5, 5),
            (-3, 2, -5),
            (0, 0, 0),
            (3.5, 1.5, 2)
        ]

        with patch.object(self.calculator, '_check_args') as mock_check_args:
            for a, b, expected_result in test_cases:
                result = self.calculator.subtract(a, b)
                self.assertEqual(result, expected_result)
                mock_check_args.assert_called_once_with(a, b)
                mock_check_args.reset_mock()

    def test_subtract_negative(self):
        test_cases = [
            ("5", 2),
            (1, None),
            ({}, 2.5)
        ]

        with patch.object(self.calculator, '_check_args') as mock_check_args:
            for a, b in test_cases:
                mock_check_args.side_effect = ValueError(ERROR_MESSAGE)
                with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                    self.calculator.subtract(a, b)
                mock_check_args.assert_called_once_with(a, b)
                mock_check_args.reset_mock()

    def test_multiply_positive(self):
        test_cases = [
            ([2, 3, 4], 24),
            ([1.5, 2.5, 3], 11.25)
        ]

        with patch.object(self.calculator, '_check_args') as mock_check_args:
            for args, expected_result in test_cases:
                result = self.calculator.multiply(*args)
                self.assertEqual(result, expected_result)
                mock_check_args.assert_called_once_with(*args)
                mock_check_args.reset_mock()

    def test_multiply_negative(self):

        with patch('calc.calculator.SimpleCalculator._check_args') as mock_check_args:
            for args in TEST_CASES_NEGATIVE:
                mock_check_args.side_effect = ValueError(ERROR_MESSAGE)
                with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                    self.calculator.multiply(*args)
                mock_check_args.assert_called_with(*args)
                mock_check_args.reset_mock()

    def test_zero_case_multiply(self):
        zero_test_case = [2, 0, 4]

        with patch.object(self.calculator, '_check_args') as mock_check_args:
            with self.assertRaises(ValueError):
                self.calculator.multiply(*zero_test_case)
                mock_check_args.assert_called_once_with(*zero_test_case)

    def test_prepare_numbers_positive(self):
        lower_threshold = 2
        upper_threshold = 4
        expected_result_if_lower, expected_result_if_upper, expected_result_if_both = [
                                                                                        [2, 3, 4, 5],
                                                                                        [1, 2, 3, 4],
                                                                                        [2, 3, 4]
        ]

        with patch('calc.calculator.SimpleCalculator._check_args') as mock_check_args:
            result = self.calculator._prepare_numbers(NUMBERS, lower_threshold=lower_threshold)
            self.assertEqual(result, expected_result_if_lower)

            result = self.calculator._prepare_numbers(NUMBERS, upper_threshold=upper_threshold)
            self.assertEqual(result, expected_result_if_upper)

            result = self.calculator._prepare_numbers(NUMBERS, lower_threshold=lower_threshold,
                                                      upper_threshold=upper_threshold)
            self.assertEqual(result, expected_result_if_both)
            mock_check_args.assert_called()
            mock_check_args.reset_mock()

    def test_prepare_numbers_negative(self):
        lower_threshold = "2"
        upper_threshold = True

        with patch.object(self.calculator, '_check_args') as mock_check_args:
            mock_check_args.side_effect = ValueError(ERROR_MESSAGE)
            with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                self.calculator._prepare_numbers(NUMBERS, lower_threshold=lower_threshold)
                mock_check_args.assert_called_once_with(lower_threshold)
                mock_check_args.reset_mock()
            with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                self.calculator._prepare_numbers(NUMBERS, upper_threshold=upper_threshold)
                mock_check_args.assert_called_once_with(upper_threshold)
                mock_check_args.reset_mock()
            with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                self.calculator._prepare_numbers(NUMBERS,
                                                 lower_threshold=lower_threshold, upper_threshold=upper_threshold)
                mock_check_args.assert_called_once_with(lower_threshold, upper_threshold)
                mock_check_args.reset_mock()

    def test_calculate_average_positive(self):
        with mock.patch.object(self.calculator, '_check_args') as mock_check_args:
            mock_check_args.return_value = None

            with mock.patch.object(self.calculator, '_prepare_numbers') as mock_prepare_numbers:
                mock_prepare_numbers.return_value = [1, 2, 3]

                result = self.calculator.calculate_average(NUMBERS)
                self.assertEqual(result, 2.0)

                mock_check_args.assert_called_once()
                mock_prepare_numbers.assert_called_once_with(NUMBERS, None, None)
                mock_check_args.reset_mock()
                mock_prepare_numbers.reset_mock()

            with mock.patch.object(self.calculator, '_prepare_numbers') as mock_prepare_numbers:
                mock_prepare_numbers.return_value = []

                result = self.calculator.calculate_average(NUMBERS)
                self.assertEqual(result, 0)

                mock_check_args.assert_called_once()
                mock_prepare_numbers.assert_called_once_with(NUMBERS, None, None)
                mock_check_args.reset_mock()
                mock_prepare_numbers.reset_mock()

    def test_calculate_average_negative(self):
        with patch.object(self.calculator, '_check_args') as mock_check_args:
            mock_check_args.side_effect = ValueError(ERROR_MESSAGE)

            for numbers in TEST_CASES_NEGATIVE:
                with self.assertRaisesRegex(ValueError, ERROR_MESSAGE):
                    self.calculator.calculate_average(numbers)

                    mock_check_args.assert_called_once_with(*numbers)
                    mock_check_args.reset_mock()


if __name__ == '__maine__':
    unittest.main()
