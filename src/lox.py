import sys
from pathlib import Path

from lox_scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from error_handler import Lox


had_err = Lox.had_error

# interprete from file
def run_file(path):
    global had_err # letting know the function that we are using global variable

    file_path = Path(path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source = file.read()
        run(source)

        if had_err:
            sys.exit(65)
        
    except FileNotFoundError: # Catching the specific error
        print(f"Error: Could not find the file '{path}'.")
        
    except IOError: # A broader catch-all for permission issues, etc.
        print(f"Error: Could not read the file '{path}'.")

# REPL (Read-Eval-Print Loop), in short reading from terminal directly
def run_prompt():
    global had_err
    
    while True:
        try:
            line = input("> ")
            run(line)
            had_err = False
        except EOFError:
            # This triggers when the user presses Ctrl+D (Mac/Linux) or Ctrl+Z (Windows)
            print() 
            break


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expression = parser.parse()

    if had_err:
        return
    
    print(AstPrinter().print(expression))

def main():
    args = sys.argv[1:] # argv[0] is script name so we ignore it

    if len(args) > 1:
        print(f"Usage: pylox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        # REPL
        run_prompt()

if __name__ == "__main__":
    main()
