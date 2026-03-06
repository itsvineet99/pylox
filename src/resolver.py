from enum import Enum, auto

from Expr import VisitorExpr, Expr
from stmt import VisitorStmt, Stmt
from error_handler import Lox

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver(VisitorExpr, VisitorStmt):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE

    ############################
    ## visit methods that resolve 
    ## variables directly 
    #############################

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    # variable declaration
    def visit_var_stmt(self, stmt): 
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)
        return None
    
    def visit_variable_expr(self, expr):
        if self.scopes and self.scopes[-1][expr.name.lexeme] is False:
            Lox.error(expr.name, "Can't read local variable in its own initializer.")
        
        self.resolve_local(expr, expr.name)
        return None

    def visit_assign_expr(self, expr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
        return None
    
    # function declaration
    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None
    
    ############################
    ## visit methods that don't 
    ## resolve variables directly 
    #############################

    def visit_expression_stmt(self, stmt):
        self.resolve(stmt.expression)
        return None
    
    def visit_if_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)
        return None
    
    def visit_print_stmt(self, stmt):
        self.resolve(stmt.expression)
        return None
    
    def visit_return_stmt(self, stmt):
        if self.current_function == FunctionType.NONE:
            Lox.error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve(stmt.value)
        return None

    def visit_while_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None
    
    def visit_binary_expr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_call_expr(self, expr):
        self.resolve(expr.callee)

        for argument in expr.arguments:
            self.resolve(argument)
        return None
    
    def visit_grouping_expr(self, expr):
        self.resolve(expr.expression)
        return None
    
    def visit_literal_expr(self, expr):
        return None
    
    def visit_logical_expr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visit_unary_expr(self, expr):
        self.resolve(expr.right)
        return None

    def visit_break_stmt(self, stmt):
        return None

    ############################
    ## tools / utility functions 
    ############################

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    # keystone method (idk why i called it that)
    def resolve(self, syntax):
        if isinstance(syntax, list):
            for statement in syntax:
                self.resolve(statement)
        if isinstance(syntax, Stmt):
            syntax.accept(self)
        if isinstance(syntax, Expr):
            syntax.accept(self)

    def resolve_local(self, expr, name):
        # reversed() walks the list backwards.
        for distance, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, distance)
                return


    def resolve_function(self, func, type):
        enclosing_function = self.current_function
        self.current_function = type

        self.begin_scope()
        for param in func.params:
            self.declare(param)
            self.define(param)

        self.resolve(func.body)
        self.end_scope()

        self.current_function = enclosing_function

    def declare(self, name):
        if not self.scopes:
            return 
        
        scope = self.scopes[-1]
        if name.lexeme in scope:
            Lox.error(name, "Already variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True
