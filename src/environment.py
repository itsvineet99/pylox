from lox_token import Token
from lox_runtime_error import LoxRuntimeError

class Environment:
    def __init__(self, enclosing: 'Environment' = None):
        self.values = {}
        self.enclosing = enclosing

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return 
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
