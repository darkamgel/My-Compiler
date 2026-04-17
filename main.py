import sys

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import LexerError, ParserError, InterpreterError
from ast_nodes import (
    Program,
    Block,
    LetStatement,
    AssignStatement,
    PrintStatement,
    IfStatement,
    WhileStatement,
    BinOp,
    UnaryOp,
    Number,
    Variable,
)


def print_header(title):
    line = "=" * 12
    print(f"{line} {title} {line}")


def print_ast(node, indent="", is_last=True):
    connector = "└── " if is_last else "├── "
    print(indent + connector + node_label(node))

    child_indent = indent + ("    " if is_last else "│   ")
    children = get_children(node)

    for i, child in enumerate(children):
        last = i == len(children) - 1
        print_ast(child, child_indent, last)


def node_label(node):
    if isinstance(node, Program):
        return "Program"
    if isinstance(node, Block):
        return "Block"
    if isinstance(node, LetStatement):
        return f"LetStatement(name={node.name})"
    if isinstance(node, AssignStatement):
        return f"AssignStatement(name={node.name})"
    if isinstance(node, PrintStatement):
        return "PrintStatement"
    if isinstance(node, IfStatement):
        return "IfStatement"
    if isinstance(node, WhileStatement):
        return "WhileStatement"
    if isinstance(node, BinOp):
        return f"BinOp(op={node.op})"
    if isinstance(node, UnaryOp):
        return f"UnaryOp(op={node.op})"
    if isinstance(node, Number):
        return f"Number(value={node.value})"
    if isinstance(node, Variable):
        return f"Variable(name={node.name})"
    return type(node).__name__


def get_children(node):
    if isinstance(node, Program):
        return node.statements
    if isinstance(node, Block):
        return node.statements
    if isinstance(node, LetStatement):
        return [node.expr]
    if isinstance(node, AssignStatement):
        return [node.expr]
    if isinstance(node, PrintStatement):
        return [node.expr]
    if isinstance(node, IfStatement):
        children = [node.condition, node.then_branch]
        if node.else_branch is not None:
            children.append(node.else_branch)
        return children
    if isinstance(node, WhileStatement):
        return [node.condition, node.body]
    if isinstance(node, BinOp):
        return [node.left, node.right]
    if isinstance(node, UnaryOp):
        return [node.operand]
    return []


def run_source(source_code, show_tokens=True, show_ast=True, trace=False):
    print_header("SOURCE CODE")
    print(source_code.strip())
    print()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    if show_tokens:
        print_header("TOKENS")
        for token in tokens:
            print(token)
        print()

    parser = Parser(tokens)
    ast = parser.parse()

    if show_ast:
        print_header("AST")
        print_ast(ast)
        print()

    print_header("PROGRAM OUTPUT")
    interpreter = Interpreter(trace=trace)
    interpreter.visit(ast)
    print()

    interpreter.print_symbol_table()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file> [--trace]")
        sys.exit(1)

    file_path = sys.argv[1]
    trace = "--trace" in sys.argv

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        run_source(
            source_code,
            show_tokens=True,
            show_ast=True,
            trace=trace
        )

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except (LexerError, ParserError, InterpreterError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()