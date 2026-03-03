from token_type import TokenType
from lox_token import Token
from Expr import *
from stmt import *
from error_handler import Lox

class ParseError(RuntimeError):
    pass

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

        self.current = 0
        self.loop_depth = 0 # to keep the track of scope

        # allowing REPL to execute expressions directly
        self.allow_expr = False
        self.found_expr = False

    # api method to use our parser from other files.
    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())

        return statements
    
     # a parse method to use in REPL so we can easily evaluate raw expressions.
    def parse_repl(self):
        self.allow_expr = True
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())

            if self.found_expr:
                last = statements[-1]
                return last.expression
            self.allow_expr = False
        
        return statements
    
    def declaration(self):
        try:
            if self.match(TokenType.FUN):
                return self.function_("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError as error:
            self.synchronize()
            return None
        
    # Note: declarations are also statements called declaration statements.
        
    ###############
    ## declarations 
    ###############

    def function_(self, kind):
        name = self.consume(TokenType.IDENTIFIER, f"expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []

        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
            
            while(self.match(TokenType.COMMA)):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")

                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body = self.block()
        return Function(name, parameters, body)
    
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)
        
    def statement(self):
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.BREAK):
            return self.break_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        else:
            return self.expression_statement()
        
    ###############
    ### statements
    ###############

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        try:
            self.loop_depth += 1
            body = self.statement()
            if increment is not None:
                body = Block(
                    [body, Expression(increment)]
                )
            
            if condition is None:
                condition = Literal(True)
            body = While(condition, body)

            if initializer is not None:
                body = Block(
                    [initializer, body]
                )

            return body
        
        finally:
            self.loop_depth -= 1

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)
    
    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON,  "Expect ';' after return value.")
        return Return(keyword, value)
    
    def expression_statement(self):
        expr = self.expression()
        # for evaluating raw expressions
        if self.allow_expr and self.is_at_end():
            self.found_expr = True
        else:
            self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)
    
    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
            
        try:    
            self.loop_depth += 1
            body = self.statement()
            return While(condition, body)
        finally:
            self.loop_depth -= 1

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)
    
    def break_statement(self):
        if self.loop_depth == 0:
            self.error(self.previous(), "Must be inside a loop to use 'break'.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after 'break'.")
        return Break()
    
    ###############
    # block / scope 
    ###############
    def block(self):
        statements = []
        
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
        
    def expression(self):
        return self.assignment()
    
    ###############
    ### expressions 
    ###############

    def assignment(self):
        expr = self.or_()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
        
            self.error(equals, "Invalid assignment target.")
        return expr
    
    def or_(self):
        expr = self.and_()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Logical(expr, operator, right)

        return expr

    def and_(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr
    
    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER,
                         TokenType.GREATER_EQUAL,
                         TokenType.LESS,
                         TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.call()
        
    def call(self):
        expr = self.primary()

        while(True):
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        
        return expr
    
    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(callee, paren, arguments)
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")

    ###########################
    ## helper functions / tools
    ###########################

    def match(self, *token_types):
        for typ in token_types:
            if self.check(typ):
                self.advance()
                return True
        return False        
    
    def consume(self, typ, message):
        if self.check(typ):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, typ):
        if self.is_at_end():
            return False
        return self.peek().token_type == typ

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        Lox.error(token, message)
        return ParseError()
    
    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return
            if self.peek().token_type in (
                TokenType.CLASS, TokenType.FUN, TokenType.VAR, 
                TokenType.FOR, TokenType.IF, TokenType.WHILE, 
                TokenType.PRINT, TokenType.RETURN
            ):
                return
            
            self.advance()
