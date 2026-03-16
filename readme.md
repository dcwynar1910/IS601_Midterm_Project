Hello and welcome to my Midterm REPL Calculator project!

This project is an advanced version of a standard calculator and has multiple useful additions.
With a standard calculator you can only do simple operations like add, subtract, divide, multiply
and others, but with this one it comes with much more.

Before we dive into how to download and use this app let us cover what this app's abilities are.
Other than the standard add, subtract, divide, multiply, this app also comes with Power, Root,
Modulus, Integer Division, Percentage, and Absolute Difference. Furthermore, we are also able to
undo and redo our actions and we can also view all the commands we entered by typing "history".
Our history comes in a csv and we can load and save it whenever we want to. That means we can take
our csv and send it over to someone else for them to see our work. For a list of all commands type
"help"

To start, create a directory for the calculator project
Next use git clone to copy down the entire project
Once the project is successfully downloaded enter into it using cd in the terminal
Once you are in let us create a Python virtual enviroment by doing python3 -m venv venv
Next activate it by doing source venv/bin/activate
There should now be a (venv) next to your username on the left!
Install dependencies: pip install -r requirements.txt
You have finished the command line set up, run python main.py to start the calculator

For the .env it is all dynamic so you do not have to worry about configuring it, although if you would like to, here are the variables
CALCULATOR_BASE_DIR
CALCULATOR_LOG_DIR
CALCULATOR_HISTORY_DIR
CALCULATOR_MAX_HISTORY_SIZE
CALCULATOR_AUTO_SAVE
CALCULATOR_PRECISION
CALCULATOR_MAX_INPUT_VALUE
CALCULATOR_DEFAULT_ENCODING
CALCULATOR_HISTORY_FILE
CALCULATOR_LOG_FILE

Create a new file called .env and assign these variables.

To use the calculator type in help first to see the list of commands. When you want to do an operation type the operation first and then 2 numbers in 2 seperate inputs.

The best way to run tests is to use pytest --cov=. --cov-report=term-missing
This shows the coverage as well as if anything is failing.

Once you have finished you can create your own repository and push this to your main branch.
This will launch GitHub actions to test the code. Only 90% and above coverage is allowed to pass.