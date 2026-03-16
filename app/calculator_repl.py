from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

def calculator_repl():
    try:
        calc = Calculator()
        ##
        print("\nWelcome to my Calculator! Enter 'help' for a list of commands")

        while True:
            try:
                command = input("\nEnter Command: ")
                command = command.lower().strip()

                if command == "help":
                    print("Help menu:")
                    print("\tAvailable Operations: \n\t\t['add', 'subtract', 'multiply', 'divide', \n\t\t'power', 'root', 'modulus', 'int_divide', \n\t\t'percent', 'abs_diff']")
                    print("\texit : Exits Calculator")
                    print("\thistory : Shows your calculation history")
                    print("\tclear : Clears history")
                    print("\tundo : Undo last calculation")
                    print("\tredo : Redo last calculation that was undone")
                    print("\tsave : Saves calculation history to csv")
                    print("\tload : Loads calculation history from csv")
                    continue

                if command == "exit":
                    try:
                        calc.save_history()
                        print("Successfully saved Calculation history")
                    except Exception as e: # pragma: no cover
                        print("There was a problem saving history:", e)
                    
                    print("Goodbye")

                    break

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_divide', 'percent', 'abs_diff']:
                    try:
                        print("Please enter number 1 and then number 2 in a seperate input")
                        a = input("First number: ").lower().strip()
                        if a == "cancel":
                            print("Calculation cancelled")
                            continue

                        b = input("Second number: ").lower().strip()
                        if b == "cancel":
                            print("Calculation cancelled")
                            continue

                        # We get a opertation class from this 
                        cur_operation = OperationFactory.create_operation(command)
                        
                        # we pass this class to calc
                        calc.set_operation(cur_operation)

                        output = calc.perform_operation(a,b)

                        print(f"Result: {output}")

                    # Here we use our created validation errors:
                    except(ValidationError, OperationError) as e:
                        print("Error:", e)
                    except Exception as e:
                        print("Unexpected Error:", e)
                    continue
            
                if command == "history":
                    cur_history = calc.show_history()
                    if not cur_history:
                        print("\nThe history is empty, there have been no commands yet")
                    else:
                        for i in cur_history:
                            print("\t",i)
                        #print(cur_history)
                    continue

                if command == "clear":
                    calc.clear_history()
                    
                    print("History cleared")
                    
                    continue

                if command == "undo":
                    if calc.undo():
                        print("Command undone!")
                    else:
                        print("Nothing to undo")
                    continue

                if command == "redo":
                    if calc.redo():
                        print("Command redone!")
                    else:
                        print("Nothing to redo")
                    continue

                if command == "save":
                    calc.save_history()
                    print("History saved!")
                    continue

                if command == "load":
                    calc.load_history()
                    print("History loaded!")
                    continue

                print(f"Unknown command: '{command}'. Type 'help' for available options.")
            except Exception as e:
                print(f"Error in entering command: {e}")
                logging.error(f"Error in entering command: {e}")
                continue

    except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error in REPL: {e}")
            raise