import time
from Expr import *
from stmt import *
from token_type import TokenType
from lox_runtime_error import LoxRuntimeError
from return_error import ReturnError
from error_handler import Lox
from environment import Environment
from lox_function import LoxFunction, LoxCallable
from lox_class import LoxClass, LoxInstance


# native function 
class Clock(LoxCallable):
    def arity(self):
        return 0
    
    def call(self, interpreter, arguments):
        return time.time()
    
    def __str__(self):
        return "<native fn>"


class BreakError(RuntimeError):
    pass

class Interpreter(VisitorExpr, VisitorStmt):
    def __init__(self):
        # permanent global scope
        self.globals_ = Environment()
        # the active environment that tracks our current scope
        self.environment = self.globals_
        # defining native functions
        self.globals_.define("clock", Clock())
        # stores expr(variable) and the number which indicates where this variable was declared 
        self.locals_ = {} # _ cause locals keyword exists in python alr.

    # API to use by other programs.
    def interpret(self, syntax):
        try:
            if isinstance(syntax, list):
                # when we are giving input as a list of statements 
                for statement in syntax:
                    self.execute(statement)
            else:
                # when we are giving input as expression (REPL interactive execution)
                value = self.evaluate(syntax)
                return self.stringify(value)
                
        except LoxRuntimeError as error:
            Lox.runtime_error(error)
            return None
        
    ################################
    ### visit methods / evaluating 
    ################################

    ##############
    ## expressions 
    ##############

    def visit_literal_expr(self, expr: Literal):
        return expr.value
    
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
                # comapares string by their length
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

    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")
        
        function = callee
        if len(arguments) != function.arity():
            raise LoxRuntimeError(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        
        return function.call(self, arguments)
    
    def visit_variable_expr(self, expr):
        return self.lookup_variable(expr.name, expr)
    
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)

        distance = self.locals_.get(id(expr))
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals_.assign(expr.name, value)
        return value
    
    def visit_get_expr(self, expr):
        obj = self.evaluate(expr.object)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)
        raise LoxRuntimeError(expr.name, "Only instances have properties.")
    
    def visit_set_expr(self, expr):
        obj = self.evaluate(expr.object)

        if not isinstance(obj, LoxInstance):
            raise LoxRuntimeError(expr.name, "Only instances have fields.")
        
        value = self.evaluate(expr.value)
        obj.set(expr.name, value)

        return value
    
    def visit_super_expr(self, expr):
        distance = self.locals_.get(id(expr))

        superclass = self.environment.get_at(distance, "super")
        obj = self.environment.get_at(distance - 1, "this")
        method = superclass.find_method(expr.method.lexeme)

        if method is None:
            raise LoxRuntimeError(expr.method, 
                                  "Undefined property '" + expr.method.lexeme + "'.")
        return method.bind(obj)
        
    def visit_this_expr(self, expr):
        return self.lookup_variable(expr.keyword, expr)
    
    #############
    ## statement
    #############
    
    def visit_expression_stmt(self, stmt) -> None:
        self.evaluate(stmt.expression)
        return None
    
    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        
        return None
    
    def visit_break_stmt(self, stmt):
        raise BreakError()
    
    def visit_print_stmt(self, stmt) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_while_stmt(self, stmt):
        try:
            while(self.is_truthy(self.evaluate(stmt.condition))):
                self.execute(stmt.body)
        except BreakError:
            pass
        return None
    
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None
    
    def visit_function_stmt(self, stmt):
        func = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, func)
        return None
    
    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise ReturnError(value)
    
    def visit_class_stmt(self, stmt):
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise LoxRuntimeError(stmt.superclass.name, 
                                      "Superclass must be a name.")

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)
        
        methods = {}
        for method in stmt.methods:
            func = LoxFunction(method, self.environment,
                               method.name.lexeme == "init")
            methods[method.name.lexeme] = func

        klass = LoxClass(stmt.name.lexeme, superclass, methods)

        if stmt.superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, klass)

        return None
    
    ####################
    ## helper functions
    ####################

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
        
    def resolve(self, expr, depth):
        self.locals_[id(expr)] = depth

    def lookup_variable(self, name, expr):
        distance = self.locals_.get(id(expr)) # didn't know that dict has .get syntax too TT
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals_.get(name)
