import sys

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import LexerError, ParserError, InterpreterError
from ast_nodes import (
    Program,
    LetStatement,
    AssignStatement,
    PrintStatement,
    BinOp,
    UnaryOp,
    Number,
    Variable,
)


def print_ast(node, indent=0):
    prefix = "  " * indent

    if isinstance(node, Program):
        print(f"{prefix}Program")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)

    elif isinstance(node, LetStatement):
        print(f"{prefix}LetStatement(name={node.name})")
        print_ast(node.expr, indent + 1)

    elif isinstance(node, AssignStatement):
        print(f"{prefix}AssignStatement(name={node.name})")
        print_ast(node.expr, indent + 1)

    elif isinstance(node, PrintStatement):
        print(f"{prefix}PrintStatement")
        print_ast(node.expr, indent + 1)

    elif isinstance(node, BinOp):
        print(f"{prefix}BinOp(op={node.op})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, UnaryOp):
        print(f"{prefix}UnaryOp(op={node.op})")
        print_ast(node.operand, indent + 1)

    elif isinstance(node, Number):
        print(f"{prefix}Number(value={node.value})")

    elif isinstance(node, Variable):
        print(f"{prefix}Variable(name={node.name})")


def run_source(source_code, show_tokens=True, show_ast=True):
    print("===== SOURCE CODE =====")
    print(source_code.strip())
    print()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    if show_tokens:
        print("===== TOKENS =====")
        for token in tokens:
            print(token)
        print()

    parser = Parser(tokens)
    ast = parser.parse()

    if show_ast:
        print("===== AST =====")
        print_ast(ast)
        print()

    print("===== OUTPUT =====")
    interpreter = Interpreter()
    interpreter.visit(ast)
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        run_source(source_code, show_tokens=True, show_ast=True)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except (LexerError, ParserError, InterpreterError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()