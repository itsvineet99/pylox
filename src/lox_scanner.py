from token_type import TokenType
from lox_token import Token
from error_handler import Lox

# all keywords in lox
KEYWORDS = {
    "and":    TokenType.AND,
    "class":  TokenType.CLASS,
    "else":   TokenType.ELSE,
    "false":  TokenType.FALSE,
    "for":    TokenType.FOR,
    "fun":    TokenType.FUN,
    "if":     TokenType.IF,
    "nil":    TokenType.NIL,
    "or":     TokenType.OR,
    "print":  TokenType.PRINT,
    "return": TokenType.RETURN,
    "super":  TokenType.SUPER,
    "this":   TokenType.THIS,
    "true":   TokenType.TRUE,
    "var":    TokenType.VAR,
    "while":  TokenType.WHILE
}

class Scanner:
    def __init__(self, source):
        self.source = source

        self.start=0
        self.current = 0
        self.line = 1

        self.tokens = []

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        char = self.advance()
        
        match char:
            # single tokens
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}': 
                self.add_token(TokenType.RIGHT_BRACE)
            case ',': 
                self.add_token(TokenType.COMMA)
            case '.': 
                self.add_token(TokenType.DOT)
            case '-': 
                self.add_token(TokenType.MINUS)
            case '+': 
                self.add_token(TokenType.PLUS)
            case ';': 
                self.add_token(TokenType.SEMICOLON)
            case '*': 
                self.add_token(TokenType.STAR)
            # operators 
            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<':
                self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>':
                self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            # comments 
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            # Ignore whitespace
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            # string
            case '"':
                self.string()
            # default case
            case _: 
                if self.is_digit(char):
                    self.number()
                elif self.is_alpha(char):
                    self.identifier()
                else:
                    Lox.error(self.line, "Unexpected character.")

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]
    
    def add_token(self, token_type, literal=None):
        text = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            Lox.error(self.line, "Unterminated string.")
            return
        
        self.advance()
        value = self.source[self.start+1 : self.current-1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, char):
        return '0' <= char <= '9'

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        # Extract the number string and convert it to a float
        value = float(self.source[self.start : self.current])
        self.add_token(TokenType.NUMBER, value)

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        self.add_token(token_type)

    def is_alpha(self, char):
        return ('a' <= char <= 'z') or ('A' <= char <= 'Z') or char == '_'
    
    def is_alpha_numeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)
