from functools import reduce
from typing import List, Union


my_type = Union[int, float]


class SimpleCalculator:

    def _check_args(self, *args: object) -> None:
        """checks if all passed arguments are of type int or float."""
        if not all(isinstance(arg, my_type) for arg in args):
            raise ValueError("Аргументи повинні бути типами int або float")

    def add(self, *args: my_type) -> my_type:
        """finds the sum of all arguments"""
        self._check_args(*args)
        return sum(args)

    def subtract(self, a: my_type, b: my_type) -> my_type:
        """subtracts b from a"""
        self._check_args(a, b)
        return a - b

    def multiply(self, *args: my_type) -> my_type:
        """ finds the product of the arguments"""
        self._check_args(*args)
        if not all(args):
            raise ValueError
        return reduce(lambda x, y: x*y, args)

    def division(self, a: my_type, b: my_type) -> my_type:
        """calculates the quotient of numbers a and b"""
        self._check_args(a, b)
        try:
            return a / b
        except ZeroDivisionError:
            return float('inf')

    def _prepare_numbers(self, numbers: List[my_type],
                         lower_threshold: my_type = None, upper_threshold: my_type = None) -> List[my_type]:
        """removes numbers from the list 'numbers' that are outside the lower and upper threshold"""
        _prepared_numbers = numbers
        if lower_threshold is not None:
            self._check_args(lower_threshold)
            _prepared_numbers = [x for x in _prepared_numbers if x >= lower_threshold]

        if upper_threshold is not None:
            self._check_args(upper_threshold)
            _prepared_numbers = [x for x in _prepared_numbers if x <= upper_threshold]

        return _prepared_numbers

    def calculate_average(self, numbers: List[my_type],
                          lower_threshold: my_type = None, upper_threshold: my_type = None) -> my_type:
        """calculates the average of numbers"""
        self._check_args(*numbers)
        _prepared_numbers = self._prepare_numbers(numbers, lower_threshold, upper_threshold)
        if not len(_prepared_numbers):
            return 0
        else:
            return sum(_prepared_numbers)/len(_prepared_numbers)
