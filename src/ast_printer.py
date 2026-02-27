from Expr import *
from token_type import TokenType

class AstPrinter(VisitorExpr):
    def print(self, expr: Expr):
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    # A helper method to handle the LISP-style string formatting
    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        # We use a list to build the string piece by piece
        builder = [f"({name}"]
        
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
            
        builder.append(")")
        return "".join(builder)

def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )

    print(AstPrinter().print(expression))

if __name__ == "__main__":
    main()
