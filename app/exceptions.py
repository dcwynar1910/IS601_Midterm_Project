class CalculatorError(Exception): # This creates a hierachy of Execeptions in the calculator
    pass

class ValidationError(CalculatorError):
    pass

class OperationError(CalculatorError):
    pass

class ConfigurationError(CalculatorError):
    pass