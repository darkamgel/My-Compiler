"""
Semantic analyzer for the toy programming language.

This module performs semantic checking on the Abstract Syntax Tree (AST)
after parsing and before interpretation. Its purpose is to catch meaning-related
errors that are not handled by the lexer or parser, such as using variables
before declaration or declaring the same variable more than once.

Main responsibilities:
- Ensure variables are declared before they are used
- Prevent duplicate variable declarations
- Validate assignments only to previously declared variables
- Recursively analyze expressions, statements, and control-flow blocks
- Raise clear semantic errors when program rules are violated

The analyzer uses a visitor-style approach to walk through each AST node
and maintains a symbol table-like set to track declared variable names.

Overall, this module acts as the semantic validation stage in the pipeline:
    Tokens → Parser → AST → Semantic Analyzer → Interpreter

By checking the program before execution, it helps prevent runtime issues
caused by invalid variable usage and improves overall language reliability.
"""

from ast_nodes import (
    Program,
    Block,
    Number,
    String,
    Variable,
    BinOp,
    UnaryOp,
    LetStatement,
    AssignStatement,
    PrintStatement,
    InputExpression,
    IfStatement,
    WhileStatement,
    ForStatement,
)
from errors import SemanticError


class SemanticAnalyzer:
    """
    Simple semantic analyzer.

    Checks:
    - variable must be declared before use
    - duplicate declaration is not allowed
    """

    def __init__(self):
        self.symbols = set()

    def analyze(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        method(node)

    def no_visit_method(self, node):
        raise SemanticError(f"No semantic rule for {type(node).__name__}")

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.analyze(stmt)

    def visit_Block(self, node: Block):
        for stmt in node.statements:
            self.analyze(stmt)

    def visit_Number(self, node: Number):
        pass

    def visit_String(self, node: String):
        pass

    def visit_Variable(self, node: Variable):
        if node.name not in self.symbols:
            raise SemanticError(f"Variable '{node.name}' used before declaration")

    def visit_BinOp(self, node: BinOp):
        self.analyze(node.left)
        self.analyze(node.right)

    def visit_UnaryOp(self, node: UnaryOp):
        self.analyze(node.operand)

    def visit_LetStatement(self, node: LetStatement):
        if node.name in self.symbols:
            raise SemanticError(f"Variable '{node.name}' already declared")
        self.analyze(node.expr)
        self.symbols.add(node.name)

    def visit_AssignStatement(self, node: AssignStatement):
        if node.name not in self.symbols:
            raise SemanticError(f"Variable '{node.name}' assigned before declaration")
        self.analyze(node.expr)

    def visit_PrintStatement(self, node: PrintStatement):
        self.analyze(node.expr)

    def visit_InputExpression(self, node: InputExpression):
        if node.prompt is not None:
            self.analyze(node.prompt)

    def visit_IfStatement(self, node: IfStatement):
        self.analyze(node.condition)
        self.analyze(node.then_branch)
        if node.else_branch is not None:
            self.analyze(node.else_branch)

    def visit_WhileStatement(self, node: WhileStatement):
        self.analyze(node.condition)
        self.analyze(node.body)

    def visit_ForStatement(self, node: ForStatement):
        self.analyze(node.init)
        self.analyze(node.condition)
        self.analyze(node.update)
        self.analyze(node.body)