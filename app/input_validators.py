from dataclasses import dataclass
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from decimal import Decimal, InvalidOperation

@dataclass
class InputValidator:

    @staticmethod
    def validate_number(value, config):
        try:
            value_normalized = Decimal(str(value).strip())

            if value_normalized > config.max_input_value:
                raise ValidationError("Value exceeds maximum allowed:", config.max_input_value)
            return value_normalized.normalize()
        
        except InvalidOperation as e:
            raise ValidationError("Invalid number format:", value) from e
        

