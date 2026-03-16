import datetime
from decimal import Decimal, InvalidOperation
from dataclasses import dataclass, field
import logging
from app.exceptions import OperationError

@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    solution: Decimal = field(init = False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.solution = self.calculate()

    def calculate(self):
        operations_dict = {
            "Addition" : lambda a,b : a+b,
            "Subtraction" : lambda a,b : a-b,
            "Multiplication" : lambda a,b : a*b,
            "Division" : lambda a,b : a/b,
            "Power" : lambda a,b : a**b,
            "Root" : lambda a,b : a**(1/b),
            "Modulus" : lambda a,b : a%b,
            "Integer_Division" : lambda a,b : a//b,
            "Percentage" : lambda a,b : (a/b)*100,
            "Absolute_Difference" : lambda a,b : abs(a-b)
            }
        
        try:
            cur_operation = operations_dict[self.operation]

        except:
            raise OperationError("Unknown operation:" ,self.operation)

        
        try:
            return cur_operation(self.operand1, self.operand2)
        except (ValueError, TypeError) as e:
            raise OperationError("Calculation failed:", {str(e)})


    @staticmethod
    def from_dict(data):
        try:
            calc = Calculation(
                operation = data["operation"],
                operand1= Decimal(data["operand1"]),
                operand2= Decimal(data["operand2"])
            )

            saved_result = Decimal(data['solution'])
            if calc.solution != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.solution}"
                )  # pragma: no cover

            return calc
        
        except (KeyError, ValueError, InvalidOperation) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")


    def __str__(self):
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.solution}" 
    

    def __repr__(self):
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"solution={self.solution}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )
    
    def format_result(self, precision = 10):
        try:
            return str(self.solution.quantize(Decimal("0." + "0" * precision)))
        except: # pragma: no cover
            return str(self.solution)
        
    def __eq__(self, other):
   
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.solution == other.solution
        )




