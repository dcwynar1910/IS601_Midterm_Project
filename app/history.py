from abc import ABC, abstractmethod
import logging
from app.calculation import Calculation

class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation):
        pass # pragma: no cover


class LoggingObserver(HistoryObserver):
    def update(self, calculation):
        if calculation == None or calculation is None:
            raise AttributeError("This calculation cannot be None")
        
        logging.info(f"Calculation Performed: {calculation.operation} "
                    f"({calculation.operand1}, {calculation.operand2}) = "
                    f"{calculation.result}")
        


class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator):
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation):
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")



