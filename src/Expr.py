from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from lox_token import Token

class VisitorExpr(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: 'Assign') -> Any:
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: 'Binary') -> Any:
        pass

    @abstractmethod
    def visit_call_expr(self, expr: 'Call') -> Any:
        pass

    @abstractmethod
    def visit_get_expr(self, expr: 'Get') -> Any:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: 'Grouping') -> Any:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: 'Literal') -> Any:
        pass

    @abstractmethod
    def visit_logical_expr(self, expr: 'Logical') -> Any:
        pass

    @abstractmethod
    def visit_set_expr(self, expr: 'Set') -> Any:
        pass

    @abstractmethod
    def visit_this_expr(self, expr: 'This') -> Any:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: 'Unary') -> Any:
        pass

    @abstractmethod
    def visit_variable_expr(self, expr: 'Variable') -> Any:
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: VisitorExpr) -> Any:
        pass

@dataclass(frozen=True)
class Assign(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_assign_expr(self)

@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_binary_expr(self)

@dataclass(frozen=True)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_call_expr(self)

@dataclass(frozen=True)
class Get(Expr):
    object: Expr
    name: Token

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_get_expr(self)

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
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_logical_expr(self)

@dataclass(frozen=True)
class Set(Expr):
    object: Expr
    name: Token
    value: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_set_expr(self)

@dataclass(frozen=True)
class This(Expr):
    keyword: Token

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_this_expr(self)

@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_unary_expr(self)

@dataclass(frozen=True)
class Variable(Expr):
    name: Token

    def accept(self, visitor: VisitorExpr) -> Any:
        return visitor.visit_variable_expr(self)

