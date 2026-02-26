from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from lox_token import Token
from Expr import * # we add this manually, cause our tool does not generate this line.

class VisitorStmt(ABC):
    @abstractmethod
    def visit_expression_stmt(self, stmt: 'Expression') -> Any:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: 'Print') -> Any:
        pass

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: VisitorStmt) -> Any:
        pass

@dataclass(frozen=True)
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: VisitorStmt) -> Any:
        return visitor.visit_expression_stmt(self)

@dataclass(frozen=True)
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: VisitorStmt) -> Any:
        return visitor.visit_print_stmt(self)

