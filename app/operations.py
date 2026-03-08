from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError


class Operation(ABC):
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        pass

    def validate_operands(self, a: Decimal, b: Decimal)-> Decimal:
        pass

    def __str__(self):
        return self.__class__.__name__
    


class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return a + b
    
class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return a - b
    
class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return a * b
    
class Division(Operation):
    def validate_operands(self, a, b):
        super().validate_operands(a, b)

        # check for b == 0
        if b == 0:
            raise ValidationError("Division by zero is not allowed")
    
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return a / b
    
class Power(Operation):
    def validate_operands(self, a, b):
        super().validate_operands(a, b)

        # check for b < 0
        if b < 0:
            raise ValidationError("Negative power is not allowed")
    
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return pow(a, b)
    
class Root(Operation):
    def validate_operands(self, a, b):
        super().validate_operands(a, b)

        # check for a < 0
        if a < 0:
            raise ValidationError("Root of negative number is not allowed")
        
        if b==0:
            raise ValidationError("Degree of zero is not allowed")
    
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return pow(a, (1/b))
    
class Modulus(Operation):
    def validate_operands(self, a, b):
        super().validate_operands(a, b)

        # check for b == 0
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed")
    
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return a%b
    
class Integer_Division(Operation):
    def validate_operands(self, a, b):
        super().validate_operands(a, b)

        # check for b == 0
        if b == 0:
            raise ValidationError("Integer Division by zero is not allowed")
    
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return a//b
    
class Percentage(Operation):
    def validate_operands(self, a, b):
        super().validate_operands(a, b)

        # check for b == 0
        if b == 0:
            raise ValidationError("Division by zero is not allowed in calculating percentage")
    
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return (a/b) * 100
    
class Absolute_Difference(Operation):  
    def execute(self, a: Decimal, b: Decimal)-> Decimal:
        self.validate_operands(a,b)
        return abs(a - b)




class OperationFactory:

    available_operations = {
        "add" : Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": Integer_Division,
        "percent": Percentage,
        "abs_diff": Absolute_Difference
    }

    # Registers a new operation by checking if the subclass is Operation
    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls.available_operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        create_operation_class = cls.available_operations.get(operation_type.lower())

        if not create_operation_class:
            raise ValueError("Invalid operation:", operation_type)
        
        return create_operation_class()