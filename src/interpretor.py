from Expr import *
from token_type import TokenType
from lox_runtime_error import LoxRuntimeError
from error_handler import Lox

RuntimeError
class Interpretor(Visitor):

    def visit_literal_expr(self, expr: Literal):
        return expr.value
    
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
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
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
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)


    
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

    # API to use by other programs.
    def interpret(self, expr):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            Lox.runtime_error(error)
            
