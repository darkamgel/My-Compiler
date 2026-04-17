from dataclasses import dataclass
from typing import List


class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class Number(ASTNode):
    value: float


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