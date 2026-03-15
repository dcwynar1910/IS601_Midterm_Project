import datetime
from decimal import Decimal
from dataclasses import dataclass
import logging
from app.exceptions import OperationError

@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    solution: Decimal
    timestamp: datetime.datetime = datetime.datetime.now

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
            "Percentage" : lambda a,b : (a*b)*100,
            "Absolute_Difference" : lambda a,b : abs(a-b)
            }
        
        try:
            cur_operation = operations_dict[self.operation]

        except:
            raise OperationError("Unknown operation:" ,self.operation)

        
        try:
            return cur_operation(self.operand1, self.operand2)
        except (ValueError) as e:
            raise OperationError("Calculation failed:", {str(e)})


    @staticmethod
    def from_dict(data):
        try:
            calc = Calculation(
                operation = data["operation"],
                operand1= data["operand1"],
                operand2= data["operand2"]
            )

            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.solution}"
                )  # pragma: no cover

            return calc
        
        except (KeyError, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")


    def __str__(self):
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.solution}" 
    

    def __repr__(self):
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.solution}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )
    
    def format_result(self, precision = 10):
        try:
            return str(self.solution.quantize(Decimal("0." + "0" * precision)))
        except:
            return str(self.solution)




