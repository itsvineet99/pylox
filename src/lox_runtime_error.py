# Evaluating Expressions runtime-error-class
from lox_token import Token

class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token
