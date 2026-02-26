import sys
from lox_token import Token, TokenType
from lox_runtime_error import LoxRuntimeError 

# separate file for error handling cause the original method was causing 
# cirucular error import 

class Lox:
    had_error = False
    had_runtime_error = False

    @classmethod
    def error(cls, target, message: str):
        """
        'target' can be either a line number (int) or a Token object.
        """
        if isinstance(target, int):
            # Handles: def error(line_no: int, message: str)
            cls.report(target, "", message)
            
        elif isinstance(target, Token): 
            # Handles: def error(token Token, message: str)
            if target.token_type == TokenType.EOF:
                cls.report(target.line_no, " at end", message)
            else:
                cls.report(target.line_no, f" at '{target.lexeme}'", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        # file=sys.stderr prints this to the standard error stream
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        cls.had_error = True
    
    @classmethod
    def runtime_error(cls, error: LoxRuntimeError):
        # str(error) automatically extracts the message we passed 
        # to super().__init__(message) in our custom exception class
        print(f"{str(error)}\n[line {error.token.line_no}]", file=sys.stderr)
        cls.had_runtime_error = True
