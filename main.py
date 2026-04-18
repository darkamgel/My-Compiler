"""
Main driver file for the toy compiler/interpreter.

This module connects all major stages of the language pipeline,
including lexical analysis, parsing, semantic analysis, AST
visualization, and program execution. It acts as the entry point
for running source files written in the toy language.

Main responsibilities:
- Read source code from an input file
- Generate tokens using the lexer
- Build the Abstract Syntax Tree (AST) using the parser
- Perform semantic validation before execution
- Display tokens and AST for debugging and learning purposes
- Execute the program using the interpreter
- Show runtime output and final symbol table
- Handle compiler/interpreter errors in a clear way

Additional features:
- Optional execution tracing with the --trace flag
- Optional disabling of colored terminal output with --no-color
- Tree-style AST printing for better visualization of program structure

Overall, this file serves as the controller of the full compiler workflow:
    Source File → Lexer → Parser → Semantic Analyzer → Interpreter → Output
"""

import sys

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter, Color
from errors import LexerError, ParserError, SemanticError, InterpreterError
from ast_nodes import (
    Program,
    Block,
    LetStatement,
    AssignStatement,
    PrintStatement,
    InputExpression,
    IfStatement,
    WhileStatement,
    ForStatement,
    BinOp,
    UnaryOp,
    Number,
    String,
    Variable,
)


def color(text, code, use_color=True):
    if use_color:
        return f"{code}{text}{Color.RESET}"
    return text


def print_header(title, use_color=True):
    line = "=" * 12
    print(color(f"{line} {title} {line}", Color.CYAN, use_color))


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
    if isinstance(node, InputExpression):
        return "InputExpression"
    if isinstance(node, IfStatement):
        return "IfStatement"
    if isinstance(node, WhileStatement):
        return "WhileStatement"
    if isinstance(node, ForStatement):
        return "ForStatement"
    if isinstance(node, BinOp):
        return f"BinOp(op={node.op})"
    if isinstance(node, UnaryOp):
        return f"UnaryOp(op={node.op})"
    if isinstance(node, Number):
        return f"Number(value={node.value})"
    if isinstance(node, String):
        return f'String(value="{node.value}")'
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
    if isinstance(node, InputExpression):
        return [node.prompt] if node.prompt is not None else []
    if isinstance(node, IfStatement):
        children = [node.condition, node.then_branch]
        if node.else_branch is not None:
            children.append(node.else_branch)
        return children
    if isinstance(node, WhileStatement):
        return [node.condition, node.body]
    if isinstance(node, ForStatement):
        return [node.init, node.condition, node.update, node.body]
    if isinstance(node, BinOp):
        return [node.left, node.right]
    if isinstance(node, UnaryOp):
        return [node.operand]
    return []


def print_ast(node, indent="", is_last=True):
    connector = "└── " if is_last else "├── "
    print(indent + connector + node_label(node))

    child_indent = indent + ("    " if is_last else "│   ")
    children = get_children(node)
    for i, child in enumerate(children):
        print_ast(child, child_indent, i == len(children) - 1)


def run_source(source_code, show_tokens=True, show_ast=True, trace=False, use_color=True):
    print_header("SOURCE CODE", use_color)
    print(source_code.strip())
    print()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    if show_tokens:
        print_header("TOKENS", use_color)
        for token in tokens:
            print(token)
        print()

    parser = Parser(tokens)
    ast = parser.parse()

    print_header("SEMANTIC ANALYSIS", use_color)
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print(color("Semantic analysis passed.", Color.GREEN, use_color))
    print()

    if show_ast:
        print_header("AST", use_color)
        print_ast(ast)
        print()

    print_header("PROGRAM OUTPUT", use_color)
    interpreter = Interpreter(trace=trace, color=use_color)
    interpreter.visit(ast)
    print()
    interpreter.print_symbol_table()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file> [--trace] [--no-color]")
        sys.exit(1)

    file_path = sys.argv[1]
    trace = "--trace" in sys.argv
    use_color = "--no-color" not in sys.argv

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        run_source(
            source_code,
            show_tokens=True,
            show_ast=True,
            trace=trace,
            use_color=use_color
        )

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except (LexerError, ParserError, SemanticError, InterpreterError) as e:
        print(color(f"Error: {e}", Color.RED, use_color))


if __name__ == "__main__":
    main()