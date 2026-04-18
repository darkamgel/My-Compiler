"""
Abstract Syntax Tree (AST) node definitions for the toy compiler/interpreter.

This file defines the core data structures used to represent the parsed
source program after syntactic analysis. Each class in this module models
a specific language construct, allowing later compiler stages such as
semantic analysis, interpretation, optimization, or code generation to
traverse and process the program in a structured way.

Overview:
- ASTNode:
    Base class for all AST elements.

- Program:
    Root node representing the entire source program as a sequence of statements.

- Block:
    Represents a grouped sequence of statements, typically used inside control
    flow constructs such as if, while, and for.

- Number:
    Numeric literal node storing integer or floating-point values.

- String:
    String literal node storing textual values.

- Variable:
    Represents an identifier reference, used when reading the value of a variable.

- BinOp:
    Binary operation node for expressions involving two operands, such as:
    arithmetic (+, -, *, /), comparison (==, !=, <, >, <=, >=),
    and logical operators (&&, ||).

- UnaryOp:
    Unary operation node for expressions with one operand, such as negation (-x)
    or logical not (!x).

- LetStatement:
    Variable declaration statement that introduces a new variable and assigns
    it an initial value.

- AssignStatement:
    Variable reassignment statement that updates the value of an existing variable.

- PrintStatement:
    Output statement that evaluates an expression and prints its result.

- InputExpression:
    Expression node representing user input, optionally with a prompt message.

- IfStatement:
    Conditional control-flow statement with a condition, a required then-branch,
    and an optional else-branch.

- WhileStatement:
    Loop statement that repeatedly executes a block while its condition remains true.

- ForStatement:
    Loop statement consisting of initialization, loop condition, update expression,
    and loop body.

Purpose:
This module serves as the structural foundation of the language implementation.
The parser builds instances of these nodes, and the interpreter or compiler
consumes them to execute or translate the program.

Design Notes:
- Python dataclasses are used to keep node definitions clean and concise.
- Type hints improve readability and make the compiler easier to maintain.
- The hierarchy is intentionally simple so future language features can be
  added with minimal changes.

Typical compiler pipeline usage:
    Source Code -> Lexer -> Parser -> AST (this file) -> Semantic Analysis
    -> Interpretation / Code Generation
"""

from dataclasses import dataclass
from typing import List, Optional


class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


@dataclass
class Number(ASTNode):
    value: float


@dataclass
class String(ASTNode):
    value: str


@dataclass
class Variable(ASTNode):
    name: str


@dataclass
class BinOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    op: str
    operand: ASTNode


@dataclass
class LetStatement(ASTNode):
    name: str
    expr: ASTNode


@dataclass
class AssignStatement(ASTNode):
    name: str
    expr: ASTNode


@dataclass
class PrintStatement(ASTNode):
    expr: ASTNode


@dataclass
class InputExpression(ASTNode):
    prompt: Optional[ASTNode]


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: Block
    else_branch: Optional[Block]


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Block


@dataclass
class ForStatement(ASTNode):
    init: ASTNode
    condition: ASTNode
    update: ASTNode
    body: Block