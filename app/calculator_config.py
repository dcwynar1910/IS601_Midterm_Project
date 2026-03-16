from dotenv import load_dotenv
from app.exceptions import ConfigurationError
from pathlib import Path
import os
from decimal import Decimal
from dataclasses import dataclass

load_dotenv()

@dataclass
class CalculatorConfig:

    def __init__(self,
        base_dir = None,
        log_dir = None,
        history_dir = None,
        max_history_size = None,
        auto_save = None,
        precision = None,
        max_input_value = None,
        default_encoding = None):

        self.base_dir = Path(base_dir) if base_dir is not None else Path(os.getenv("CALCULATOR_BASE_DIR", self.get_path_proj()))

        self.log_dir = Path(log_dir) if log_dir is not None else Path(os.getenv("CALCULATOR_LOG_DIR", str(self.base_dir / "logs")))
        self.history_dir = Path(history_dir) if history_dir is not None else Path(os.getenv("CALCULATOR_HISTORY_DIR", str(self.base_dir / "history")))

        self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000")) if max_history_size is None else max_history_size
        
        if auto_save != None:
            self.auto_save = auto_save
        else: 
            self.auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
         
        self.precision = int(os.getenv("CALCULATOR_PRECISION", "10")) if precision is None else precision
        self.max_input_value = Decimal(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e999")) if max_input_value is None else max_input_value
        self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8") if default_encoding is None else default_encoding
    
    @property
    def return_log_dir(self):
        return self.log_dir
    
    @property
    def return_history_dir(self):
        return self.history_dir
    
    @property
    def return_history_file(self):
        return  Path(os.getenv("CALCULATOR_HISTORY_FILE", str(self.history_dir / "calculator_history.csv")))

    @property
    def return_log_file(self):
        return  Path(os.getenv("CALCULATOR_LOG_FILE", str(self.log_dir / "calculator.log")))
 

    def validate(self):
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")
        
    #@staticmethod
    def get_path_proj(self):
        return Path(__file__).parent.parent
    




