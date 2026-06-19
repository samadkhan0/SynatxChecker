"""
Lexer (Tokenizer) for the Simple Arithmetic Expression Syntax Checker
Compiler Construction Project

Converts a raw source string into a list of Tokens.
"""

import re


class TokenType:
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'


class Token:
    def __init__(self, type_, value, position):
        self.type = type_
        self.value = value
        self.position = position  # column index in the source string

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, pos={self.position})"


class LexerError(Exception):
    def __init__(self, message, position):
        self.message = message
        self.position = position
        super().__init__(message)


# Order matters: longer / more specific patterns first.
TOKEN_SPEC = [
    (r'\d+(\.\d+)?', TokenType.NUMBER),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
    (r'\+', TokenType.PLUS),
    (r'-', TokenType.MINUS),
    (r'\*', TokenType.MULTIPLY),
    (r'/', TokenType.DIVIDE),
    (r'\(', TokenType.LPAREN),
    (r'\)', TokenType.RPAREN),
]

_MASTER_PATTERN = re.compile(
    '|'.join(f'(?P<T{i}>{pattern})' for i, (pattern, _) in enumerate(TOKEN_SPEC))
)
_GROUP_TO_TYPE = {f'T{i}': type_ for i, (_, type_) in enumerate(TOKEN_SPEC)}


def tokenize(source):
    """Turn a source string into a list of Tokens, ending with an EOF token."""
    tokens = []
    pos = 0
    length = len(source)

    while pos < length:
        ch = source[pos]

        if ch.isspace():
            pos += 1
            continue

        match = _MASTER_PATTERN.match(source, pos)
        if match is None:
            raise LexerError(f"Illegal character {ch!r}", pos)

        token_type = _GROUP_TO_TYPE[match.lastgroup]
        value = match.group()
        tokens.append(Token(token_type, value, pos))
        pos = match.end()

    tokens.append(Token(TokenType.EOF, None, pos))
    return tokens


if __name__ == '__main__':
    # quick manual test
    for t in tokenize("x + 3 * (y - 2)"):
        print(t)
