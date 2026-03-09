from lox_function import LoxCallable
from lox_runtime_error import LoxRuntimeError

class LoxClass(LoxCallable):
    def __init__(self, name, methods: dict):
        self.name = name
        self.methods = methods
    
    def find_method(self, name):
        if name in self.methods:
            return self.methods.get(name)
        return None
    
    def call(self, interpreter, arguments):
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance
    
    def arity(self):
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        
        return initializer.arity()
    
    def __str__(self):
        return self.name

class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)
        
        method = self.klass.find_method(name.lexeme)
        if method is not None: 
            return method.bind(self)

        raise LoxRuntimeError(
            name, "Undefined property '" + name.lexeme + "'."
        )
    
    def set(self, name, value):
        self.fields[name.lexeme] = value
        # debugging lines, hehe :)
        # print(f"added {name.lexeme} = {value} in a fucking class.")
        # print(f"printing fields:\n {self.fields}")

    def __str__(self):
        return self.klass.name + " instance"
