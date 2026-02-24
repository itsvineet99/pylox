from token_type import TokenType
from lox_token import Token
from Expr import *
from error_handler import Lox


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None
        
    def expression(self):
        return self.equality()
    
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
        return self.primary()
        
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")

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
            if self.peek().type in (
                TokenType.CLASS, TokenType.FUN, TokenType.VAR, 
                TokenType.FOR, TokenType.IF, TokenType.WHILE, 
                TokenType.PRINT, TokenType.RETURN
            ):
                return
            
            self.advance()


class ParseError(RuntimeError):
    pass
