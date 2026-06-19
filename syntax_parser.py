"""
Recursive-Descent Parser for the Simple Arithmetic Expression Syntax Checker
Compiler Construction Project

Grammar (left recursion removed so it can be parsed top-down):

    expression -> term ((PLUS | MINUS) term)*
    term       -> factor ((MULTIPLY | DIVIDE) factor)*
    factor     -> (PLUS | MINUS) factor
                | NUMBER
                | IDENTIFIER
                | LPAREN expression RPAREN

Original ambiguous left-recursive grammar (for the report/viva):

    E -> E + T | E - T | T
    T -> T * F | T / F | F
    F -> ( E ) | NUMBER | IDENTIFIER
"""

from lexer import tokenize, TokenType, LexerError


class ParserSyntaxError(Exception):
    def __init__(self, message, position):
        self.message = message
        self.position = position
        super().__init__(message)


class ASTNode:
    def __init__(self, type_, value=None, children=None):
        self.type = type_
        self.value = value
        self.children = children or []

    def __repr__(self, level=0):
        indent = '  ' * level
        text = f"{indent}{self.type}"
        if self.value is not None:
            text += f"({self.value})"
        text += '\n'
        for child in self.children:
            text += child.__repr__(level + 1)
        return text


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        token = self.tokens[self.pos]
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def expect(self, type_):
        token = self.current()
        if token.type != type_:
            raise ParserSyntaxError(
                f"Expected '{type_}' but found '{token.type}'"
                + (f" ({token.value!r})" if token.value is not None else ""),
                token.position,
            )
        return self.advance()

    def parse(self):
        node = self.expression()
        if self.current().type != TokenType.EOF:
            raise ParserSyntaxError(
                f"Unexpected token {self.current().value!r} after a complete expression",
                self.current().position,
            )
        return node

    # expression -> term ((PLUS | MINUS) term)*
    def expression(self):
        node = self.term()
        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance()
            right = self.term()
            node = ASTNode('BinOp', op.value, [node, right])
        return node

    # term -> factor ((MULTIPLY | DIVIDE) factor)*
    def term(self):
        node = self.factor()
        while self.current().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.advance()
            right = self.factor()
            node = ASTNode('BinOp', op.value, [node, right])
        return node

    # factor -> (PLUS|MINUS) factor | NUMBER | IDENTIFIER | LPAREN expression RPAREN
    def factor(self):
        token = self.current()

        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.advance()
            operand = self.factor()
            return ASTNode('UnaryOp', token.value, [operand])

        if token.type == TokenType.NUMBER:
            self.advance()
            return ASTNode('Number', token.value)

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return ASTNode('Identifier', token.value)

        if token.type == TokenType.LPAREN:
            self.advance()
            node = self.expression()
            self.expect(TokenType.RPAREN)
            return node

        raise ParserSyntaxError(
            f"Unexpected token {token.value!r}" if token.value is not None
            else "Unexpected end of input (incomplete expression)",
            token.position,
        )


def check_syntax(source):
    """
    Validate one expression string.
    Returns a tuple: (is_valid: bool, message: str, ast: ASTNode | None)
    """
    if not source.strip():
        return False, "Error: empty expression", None

    try:
        tokens = tokenize(source)
    except LexerError as e:
        pointer = ' ' * e.position + '^'
        return False, (
            f"Lexical Error at position {e.position}: {e.message}\n"
            f"{source}\n{pointer}"
        ), None

    try:
        ast = Parser(tokens).parse()
        return True, "Valid syntax", ast
    except ParserSyntaxError as e:
        pointer = ' ' * e.position + '^'
        return False, (
            f"Syntax Error at position {e.position}: {e.message}\n"
            f"{source}\n{pointer}"
        ), None
