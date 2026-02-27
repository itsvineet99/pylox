from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from lox_token import Token
from Expr import *

class VisitorStmt(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: 'Block') -> Any:
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: 'Expression') -> Any:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: 'Print') -> Any:
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: 'Var') -> Any:
        pass

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: VisitorStmt) -> Any:
        pass

@dataclass(frozen=True)
class Block(Stmt):
    statements: list[Stmt]

    def accept(self, visitor: VisitorStmt) -> Any:
        return visitor.visit_block_stmt(self)

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

@dataclass(frozen=True)
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor: VisitorStmt) -> Any:
        return visitor.visit_var_stmt(self)

