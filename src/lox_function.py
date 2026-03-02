from environment import Environment
from return_error import ReturnError
from stmt import *
from Expr import *

class LoxCallable(ABC):
    @abstractmethod
    def arity(self):
        pass
    @abstractmethod
    def call(self, interpreter, arguments: list):
        pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme,
                               arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnError as return_value:
            return return_value.value
        
        return None
    
    def arity(self):
        return len(self.declaration.params)
    
    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"

