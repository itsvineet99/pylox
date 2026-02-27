import sys
from pathlib import Path

from lox_scanner import Scanner
from parser import Parser
from error_handler import Lox
from interpreter import Interpreter
from Expr import *

# initializing interpretor globally so we can use the same object, when each REPL loop resets.
interpreter = Interpreter()

# interprete from file
def run_file(path):

    file_path = Path(path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source = file.read()
        run(source)

        if Lox.had_error:
            sys.exit(65)

        if Lox.had_runtime_error:
            sys.exit(70)
        
    except FileNotFoundError: # Catching the specific error
        print(f"Error: Could not find the file '{path}'.")
        
    except IOError: # A broader catch-all for permission issues, etc.
        print(f"Error: Could not read the file '{path}'.")

# REPL (Read-Eval-Print Loop), in short reading from terminal directly
def run_prompt():
    while True:
        try:
            line = input("> ")
            Lox.had_error = False
            
            scanner = Scanner(line)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            syntax = parser.parse_repl()

            if Lox.had_error:
                continue # ignore errors
            
            # when code is statement.
            if isinstance(syntax, list):
                interpreter.interpret(syntax)
            # when code is expression
            elif isinstance(syntax, Expr):
                result = interpreter.interpret(syntax)
                if result is not None:
                    print(f"= {result}")
        except EOFError:
            # This triggers when the user presses Ctrl+D (Mac/Linux) or Ctrl+Z (Windows)
            print() 
            break

def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    # for token in tokens: # this is to see how tokenizer works.
    #     print(token)
    parser = Parser(tokens)
    statements = parser.parse()

    if Lox.had_error:
        return
    
    interpreter.interpret(statements)

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
