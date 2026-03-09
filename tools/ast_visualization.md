## Source

```
class Cake {
  taste() {
    var adjective = 'delicious';
    print("The " + this.flavor + " cake is " + adjective + "!");
  }
}
```

---
## Ast String represenation

```
Class(name=Token(token_type=<TokenType.IDENTIFIER: 20>, lexeme='Cake', literal=None, line_no=1), methods=[Function(name=Token(token_type=<TokenType.IDENTIFIER: 20>, lexeme='taste', literal=None, line_no=2), params=[], body=[Var(name=Token(token_type=<TokenType.IDENTIFIER: 20>, lexeme='adjective', literal=None, line_no=3), initializer=Literal(value='delicious')), Print(expression=Binary(left=Binary(left=Binary(left=Binary(left=Literal(value='The '), operator=Token(token_type=<TokenType.PLUS: 8>, lexeme='+', literal=None, line_no=4), right=Get(object=This(keyword=Token(token_type=<TokenType.THIS: 36>, lexeme='this', literal=None, line_no=4)), name=Token(token_type=<TokenType.IDENTIFIER: 20>, lexeme='flavor', literal=None, line_no=4))), operator=Token(token_type=<TokenType.PLUS: 8>, lexeme='+', literal=None, line_no=4), right=Literal(value=' cake is ')), operator=Token(token_type=<TokenType.PLUS: 8>, lexeme='+', literal=None, line_no=4), right=Variable(name=Token(token_type=<TokenType.IDENTIFIER: 20>, lexeme='adjective', literal=None, line_no=4))), operator=Token(token_type=<TokenType.PLUS: 8>, lexeme='+', literal=None, line_no=4), right=Literal(value='!')))])])
```

---
## Tree Structure

```
Class
├── name: Token
│   ├── token_type: TokenType.IDENTIFIER: 20
│   ├── lexeme: "Cake"
│   ├── literal: None
│   └── line_no: 1
└── methods:
    └── [0]: Function
        ├── name: Token
        │   ├── token_type: TokenType.IDENTIFIER: 20
        │   ├── lexeme: "taste"
        │   ├── literal: None
        │   └── line_no: 2
        ├── params: []
        └── body:
            ├── [0]: Var
            │   ├── name: Token
            │   │   ├── token_type: TokenType.IDENTIFIER: 20
            │   │   ├── lexeme: "adjective"
            │   │   ├── literal: None
            │   │   └── line_no: 3
            │   └── initializer: Literal
            │       └── value: "delicious"
            └── [1]: Print
                └── expression: Binary
                    ├── left: Binary
                    │   ├── left: Binary
                    │   │   ├── left: Binary
                    │   │   │   ├── left: Literal
                    │   │   │   │   └── value: "The "
                    │   │   │   ├── operator: Token
                    │   │   │   │   ├── token_type: TokenType.PLUS: 8
                    │   │   │   │   ├── lexeme: "+"
                    │   │   │   │   ├── literal: None
                    │   │   │   │   └── line_no: 4
                    │   │   │   └── right: Get
                    │   │   │       ├── object: This
                    │   │   │       │   └── keyword: Token
                    │   │   │       │       ├── token_type: TokenType.THIS: 36
                    │   │   │       │       ├── lexeme: "this"
                    │   │   │       │       ├── literal: None
                    │   │   │       │       └── line_no: 4
                    │   │   │       └── name: Token
                    │   │   │           ├── token_type: TokenType.IDENTIFIER: 20
                    │   │   │           ├── lexeme: "flavor"
                    │   │   │           ├── literal: None
                    │   │   │           └── line_no: 4
                    │   │   ├── operator: Token
                    │   │   │   ├── token_type: TokenType.PLUS: 8
                    │   │   │   ├── lexeme: "+"
                    │   │   │   ├── literal: None
                    │   │   │   └── line_no: 4
                    │   │   └── right: Literal
                    │   │       └── value: " cake is "
                    │   ├── operator: Token
                    │   │   ├── token_type: TokenType.PLUS: 8
                    │   │   ├── lexeme: "+"
                    │   │   ├── literal: None
                    │   │   └── line_no: 4
                    │   └── right: Variable
                    │       └── name: Token
                    │           ├── token_type: TokenType.IDENTIFIER: 20
                    │           ├── lexeme: "adjective"
                    │           ├── literal: None
                    │           └── line_no: 4
                    ├── operator: Token
                    │   ├── token_type: TokenType.PLUS: 8
                    │   ├── lexeme: "+"
                    │   ├── literal: None
                    │   └── line_no: 4
                    └── right: Literal
                        └── value: "!"
```
