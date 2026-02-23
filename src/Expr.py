from dataclasses import dataclass
from typing import Any
from lox_token import Token

class Expr:
    pass

@dataclass(frozen=True)
class Binary(Expr):
   left: Expr
   operator: Token
   right: Expr

@dataclass(frozen=True)
class Grouping(Expr):
   expression: Expr

@dataclass(frozen=True)
class Literal(Expr):
   value: Any

@dataclass(frozen=True)
class Unary(Expr):
   operator: Token
   right: Expr

