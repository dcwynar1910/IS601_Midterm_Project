import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging

def test_addition():
    calc = Calculation(operation="Addition", operand1 = Decimal("10"), operand2 = Decimal("1"))
    assert calc.solution == Decimal("11")

def test_subtraction():
    calc = Calculation(operation="Subtraction", operand1 = Decimal("10"), operand2 = Decimal("1"))
    assert calc.solution == Decimal("9")

def test_multiplication():
    calc = Calculation(operation="Multiplication", operand1 = Decimal("10"), operand2 = Decimal("5"))
    assert calc.solution == Decimal("50")

def test_division():
    calc = Calculation(operation="Division", operand1 = Decimal("10"), operand2 = Decimal("5"))
    assert calc.solution == Decimal("2")

def test_power():
    calc = Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.solution == Decimal("8")

def test_root():
    calc = Calculation(operation="Root", operand1=Decimal("64"), operand2=Decimal("2"))
    assert calc.solution == Decimal("8")

def test_modulus():
    calc = Calculation(operation="Modulus", operand1=Decimal("10"), operand2=Decimal("3"))
    assert calc.solution == Decimal("1")

def test_Integer_Division():
    calc = Calculation(operation="Integer_Division", operand1=Decimal("10"), operand2=Decimal("4.5"))
    assert calc.solution == Decimal("2")

def test_Percentage():
    calc = Calculation(operation="Percentage", operand1=Decimal("1"), operand2=Decimal("10"))
    assert calc.solution == Decimal("10")

def test_Absolute_Difference():
    calc = Calculation(operation="Absolute_Difference", operand1=Decimal("-10"), operand2=Decimal("2"))
    assert calc.solution == Decimal("12")

def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation(operation="Unknown", operand1=Decimal("5"), operand2=Decimal("3"))

def test_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "solution": "5",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.solution == Decimal("5")

def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "invalid",
        "operand2": "3",
        "solution": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)

def test_format_result():
    calc = Calculation(operation="Division", operand1=Decimal("1"), operand2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"

def test_equality():
    calc1 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc2 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc3 = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3

# New Test to Cover Logging Warning
def test_from_dict_result_mismatch(caplog):
    """
    Test the from_dict method to ensure it logs a warning when the saved result
    does not match the computed result.
    """
    # Arrange
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "solution": "10",
        "timestamp": datetime.now().isoformat()
    }


    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    assert "Loaded calculation result 10 differs from computed result 5" in caplog.text

def test_unknown_number():
    with pytest.raises(OperationError, match="Calculation failed"):
        Calculation(operation="Division", operand1=("blah"), operand2=Decimal("3"))



   