# Simple Arithmetic Expression Syntax Checker
*Compiler Construction — *

A syntax checker for arithmetic expressions, built in pure Python with no external libraries: a hand-written **lexer** (tokenizer) and a hand-written **recursive-descent parser**.

It checks expressions like `x + 3 * (y - 2)` and reports whether they are syntactically valid, with the exact error position when they are not.

---

## Project Structure

```
syntax_checker/
    lexer.py         - Tokenizer: source string -> list of Tokens
    syntax_parser.py - Recursive-descent parser + check_syntax() API
    main.py          - CLI: interactive mode and file mode
    test_cases.txt   - Sample valid/invalid expressions
    README.md
```

---

## Setup

Requires only Python 3 (no installs needed).

```bash
cd syntax_checker
python3 main.py
```

---

## Usage

**Interactive mode:**

```bash
python3 main.py
> x + 3 * (y - 2)
VALID - syntax is correct
```

Type `tokens` to toggle the token stream, `tree` to toggle the parse tree, `quit` to exit.

**File mode** (checks one expression per line):

```bash
python3 main.py test_cases.txt
```

---

## The Grammar

The checker recognizes this language:

```
E -> E + T | E - T | T
T -> T * F | T / F | F
F -> ( E ) | NUMBER | IDENTIFIER
```

This grammar is **left-recursive**, which a top-down parser can't handle directly — it would recurse forever. So the implemented parser uses the standard left-recursion-elimination rewrite:

```
expression -> term ((PLUS | MINUS) term)*
term       -> factor ((MULTIPLY | DIVIDE) factor)*
factor     -> (PLUS | MINUS) factor
            | NUMBER
            | IDENTIFIER
            | LPAREN expression RPAREN
```

Each grammar rule maps directly to one method in `Parser` (`expression()`, `term()`, `factor()`), which is the defining trait of recursive descent. The `*` loops give left-associativity, and the rule ordering (expression calls term calls factor) gives `*/` higher precedence than `+-`.

---

## How It Works

1. **Lexical analysis** (`lexer.py`): a single master regex scans the source left to right, classifying each chunk as `NUMBER`, `IDENTIFIER`, an operator, or a parenthesis. Whitespace is skipped. Anything that doesn't match raises a `LexerError` with the exact character position.

2. **Syntax analysis** (`syntax_parser.py`): the `Parser` consumes the token list one token at a time (`current()` / `advance()`), calling itself recursively per the grammar above. If a token doesn't fit what the grammar expects, it raises `ParserSyntaxError` with the offending position — that's the syntax check.

3. **AST construction**: each successful parse also builds an abstract syntax tree, useful to show in a viva as proof the parser understood the structure, not just validated it.

---

## Example Output

```
Input: 3 + (4 * 2
INVALID
Syntax Error at position 10: Expected 'RPAREN' but found 'EOF'
3 + (4 * 2
          ^
```

---

---

## Possible Extensions

- Add exponentiation (`^`) with right-associativity
- Add assignment statements (`x = expr`) — turns this into a tiny language rather than just expression checking
- Generate an SLR/LR(0) parse table instead of recursive descent, to compare table-driven vs. hand-written parsing
