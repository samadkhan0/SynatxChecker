"""
Simple Arithmetic Expression Syntax Checker
Compiler Construction Project

Usage:
    python main.py                -> interactive mode
    python main.py test_cases.txt -> checks every line in a file
"""

import sys
from lexer import tokenize
from syntax_parser import check_syntax


def print_tokens(source):
    try:
        tokens = tokenize(source)
    except Exception:
        return
    print("Tokens:")
    for t in tokens[:-1]:  # skip EOF
        print(f"  {t.type:<12} {t.value}")


def check_and_report(expr, show_tokens=False, show_tree=False):
    print(f"\nInput: {expr}")
    if show_tokens:
        print_tokens(expr)

    valid, message, ast = check_syntax(expr)

    if valid:
        print("VALID   - syntax is correct")
        if show_tree and ast:
            print("Parse Tree:")
            print(ast)
    else:
        print("INVALID")
        print(message)

    return valid


def interactive_mode():
    print("=" * 55)
    print(" Simple Arithmetic Expression Syntax Checker")
    print(" Grammar: expr -> term ((+|-) term)*")
    print("          term -> factor ((*|/) factor)*")
    print("          factor -> NUMBER | IDENTIFIER | ( expr )")
    print(" Commands: 'tree' toggle parse tree, 'tokens' toggle tokens, 'quit' to exit")
    print("=" * 55)

    show_tree = False
    show_tokens = False

    while True:
        try:
            expr = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        lowered = expr.lower()
        if lowered in ('quit', 'exit'):
            break
        elif lowered == 'tree':
            show_tree = not show_tree
            print(f"Parse tree display: {'ON' if show_tree else 'OFF'}")
            continue
        elif lowered == 'tokens':
            show_tokens = not show_tokens
            print(f"Token display: {'ON' if show_tokens else 'OFF'}")
            continue
        elif not expr:
            continue

        check_and_report(expr, show_tokens, show_tree)


def file_mode(filepath):
    with open(filepath) as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    valid_count = 0
    for line in lines:
        if check_and_report(line):
            valid_count += 1

    print(f"\n{'=' * 55}")
    print(f"Summary: {valid_count}/{len(lines)} expressions valid")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_mode(sys.argv[1])
    else:
        interactive_mode()
