from dataclasses import dataclass
from typing import Any
from src.token_type import TokenType

# we use @dataclass for classes that only hold data and frozen=true 
# acts like final key work in java i.e variables defined here are imutable 
@dataclass(frozen=True)
class Token:
    token_type: TokenType
    lexeme: str
    literal: Any
    line_no: int


    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"
