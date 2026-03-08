from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
#from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

def calculator_repl():
    try:
        calc = Calculator()
        ##
        print("\nWelcome to the Calculator! Enter 'help' for a list of commands")

        while True:
            command = input("\nEnter Command: ")
            command = command.lower().strip()

            if command == "help":
                print("Help menu:")
                print("\tAvailable Operations: ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_divide', 'percent', 'abs_diff']")
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
                    #calc.save_history()
                    print("Successfully saved Calculation history")
                except Exception as e:
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

                    out = calc.perform_operation(a,b)

                    print("Result:", out)

                # Here we use our created validation errors:
                except(ValidationError, OperationError) as e:
                    print("Error:", e)
                except Exception as e:
                    print("Unexpected Error:", e)


                    
        





    except:
        pass