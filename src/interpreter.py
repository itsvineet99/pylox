from Expr import *
from stmt import *
from token_type import TokenType
from lox_runtime_error import LoxRuntimeError
from error_handler import Lox
from environment import Environment


class Interpreter(VisitorExpr, VisitorStmt):
    def __init__(self):
        super().__init__()
        self.environment = Environment()

    def visit_literal_expr(self, expr: Literal):
        return expr.value
    if (2 < 1 or 3 > 2) print "yes"; else print("no");
    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.token_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        
        return self.evaluate(expr.right)

    
    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            # runtime error handling
            self.check_number_operand(expr.operator, right)
            return -float(right)
        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)

        # this is mathematically unreachable but we still call it for fallback 
        return None
    
    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.GREATER:
                # comapres string by their length
                if isinstance(left, str) and isinstance(right, str):
                    return len(left) > len(right)
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                if isinstance(left, str) and isinstance(right, str):
                    return len(left) >= len(right)
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                if isinstance(left, str) and isinstance(right, str):
                    return len(left) < len(right)
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                if isinstance(left, str) and isinstance(right, str):
                    return len(left) <= len(right)
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)
                raise LoxRuntimeError(expr.operator, "Operands must be numbers or strings.")
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                # case: when we try to divide by 0.
                if right == 0:
                    raise LoxRuntimeError(expr.operator, "Learn your math dawg! you can't be dividing a number by 0.")
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)

    def visit_expression_stmt(self, stmt) -> None:
        self.evaluate(stmt.expression)
        return None
    
    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        
        return None
    
    def visit_print_stmt(self, stmt) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)
    
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None
    
    # this is a helper method which simply sends the expression back into the
    # interpreter’s visitor implementation:
    def evaluate(self, expr):
        return expr.accept(self)

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, obj_a, obj_b):
        return obj_a == obj_b

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")
    
    def stringify(self, value):
        if value is None:
            return "nil"
        
        if isinstance(value, bool):
            return str(value).lower()
        
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        
        return str(value)
    
    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
            
        finally:
            self.environment = previous


    # API to use by other programs.
    def interpret(self, syntax):
        try:
            if isinstance(syntax, list):
                # when we are giving input as list of statements 
                for statement in syntax:
                    self.execute(statement)
            else:
                # when we are giving input as expression (REPL interactive execution)
                value = self.evaluate(syntax)
                return self.stringify(value)
                
        except LoxRuntimeError as error:
            Lox.runtime_error(error)
            return None
            