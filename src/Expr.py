from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from lox_token import Token

class VisitorExpr(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: 'Binary') -> Any:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: 'Grouping') -> Any:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: 'Literal') -> Any:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: 'Unary') -> Any:
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: VisitorExpr) -> Any:
        pass

@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_binary_expr(self)

@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_grouping_expr(self)

@dataclass(frozen=True)
class Literal(Expr):
    value: Any

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_literal_expr(self)

@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_unary_expr(self)

