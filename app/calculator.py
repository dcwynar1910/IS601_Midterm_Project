import os
import logging
import pandas as pd
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError
from app.input_validators import InputValidator
from app.calculator_memento import CalculatorMemento


class Calculator:
    def __init__(self, config = None):
        if config == None or config is None:
            base = Path(__file__).parent.parent
            config = CalculatorConfig(base_dir=base)
            
        self.config = config    
        self.config.validate()

        self.setup_logging()
        self.setup_history()
        

        

    def setup_history(self):
        # History section for the user to use
        os.makedirs(self.config.history_dir, exist_ok = True)
        self.history = []
        self.observers = []
        self.undo_stack = []
        self.redo_stack = []
        self.cur_operation = None

        try:
            self.load_history()
        except Exception as e:
            logging.warning(f"Attempt to load history failed: {e}")

        logging.info("Initializing of calculator successful")

        
    def setup_logging(self):
        # Logging section for the developer to use
        try:
            os.makedirs(self.config.return_log_dir, exist_ok = True)
            log_file = self.config.return_log_file.resolve()

            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True  
            )
            logging.info(f"Logging initialized at: {log_file}")

        except Exception as e:
            print("Error setting up logging", e) # print instead of log
            raise


    def load_history(self):
        try:
            if self.config.return_history_file.exists():
                df = pd.read_csv(self.config.return_history_file)
                self.history = []
                
                if not df.empty:
                    for _,i in df.iterrows():
                        # pass data to from dict in Calculation class
                        loading_row = Calculation.from_dict({
                                'operation': i['operation'],
                                'operand1': i['operand1'],
                                'operand2': i['operand2'],
                                'solution': i['solution'],
                                'timestamp': i['timestamp']
                            })
                        self.history.append(loading_row)
                    logging.info(f"Completed loading {len(self.history)} rows from history")
                else:
                    logging.info("Completed loading empty history file")
            else:
                logging.info("History file not found - starting from scratch")

        except Exception as e:
            logging.error(f"Failed to load history file: {e}")
            raise OperationError(f"Failed to load history file: {e}")
        
    def save_history(self):
        try:
            self.config.history_dir.mkdir(parents=True, exist_ok=True)
            cur_history = []
            for i in self.history:
                cur_history.append({
                    'operation': str(i.operation),
                    'operand1': str(i.operand1),
                    'operand2': str(i.operand2),
                    'solution': str(i.solution),
                    'timestamp': i.timestamp.isoformat()
                })


            if cur_history != []:
                df = pd.DataFrame(cur_history)
                df.to_csv(self.config.return_history_file, index=False)
                logging.info(f"History saved successfully to: self.config.history_file")
            else:
                pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'solution', 'timestamp']
                           ).to_csv(self.config.return_history_file, index=False)
                logging.info("History saved with empty data")

        except Exception as e:
            logging.error(f"Failed to save history {e}")
            raise OperationError("Failed to save history", e)
        

    def add_observer(self, observer):
        self.observers.append(observer)
        logging.info(f"Added observer: {observer}")

    def remove_observer(self, observer):
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer}")

    def notify_observers(self, calculation):
        for i in self.observers:
            i.update(calculation)
        
        logging.info("Notified observers")

    def set_operation(self, operation):
        self.cur_operation = operation
        logging.info(f"Setting operation to: {operation}")

    def perform_operation(self, a,b):
        if self.cur_operation == None or self.cur_operation is None:
            raise OperationError("No operation was set")
        
        try:
            a = InputValidator.validate_number(a, self.config)
            b = InputValidator.validate_number(b, self.config)

            solution = self.cur_operation.execute(a, b)

            calculation = Calculation(operation = str(self.cur_operation), operand1 = a, operand2 = b)

            self.undo_stack.append(CalculatorMemento(self.history.copy()))

            self.redo_stack.clear()

            self.history.append(calculation)

            self.notify_observers(calculation)

            return solution
        
        except ValidationError:
            raise
        except Exception as e:
            logging.error(f"Operation failed to perform: {e}")
            raise OperationError("Operation failed to perform:", e)
        
    
    def get_history_dataframe(self):
        cur_history = []
        for i in self.history:
            cur_history.append({
                'operation': str(i.operation),
                'operand1': str(i.operand1),
                'operand2': str(i.operand2),
                'solution': str(i.solution),
                'timestamp': i.timestamp.isoformat()
            })
        return pd.DataFrame(cur_history)
    
    def show_history(self):
        cur_history = []
        for i in self.history:
            cur_history.append(f"{i.operation}({i.operand1}, {i.operand2}) = {i.solution}")

        return cur_history
    
    def clear_history(self):
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("Successfully cleared history")

    def undo(self):
        if not self.undo_stack:
            return False
        
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()

        #self.save_history()
        return True
    

    def redo(self):
        if not self.redo_stack:
            return False
        
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()

        #self.save_history()
        return True
    

