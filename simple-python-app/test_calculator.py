import pytest
from calculator import add, subtract, multiply, divide, is_even, factorial


class TestCalculator:
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        assert subtract(10, 5) == 5
        assert subtract(0, 5) == -5
        assert subtract(-5, -5) == 0

    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0

    def test_divide(self):
        assert divide(10, 2) == 5
        assert divide(7, 2) == 3.5
        assert divide(-6, 3) == -2

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_is_even(self):
        assert is_even(2) is True
        assert is_even(3) is False
        assert is_even(0) is True

    def test_factorial(self):
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120
        assert factorial(10) == 3628800

    def test_factorial_negative(self):
        with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
            factorial(-1)
