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
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: Block
    else_branch: Optional[Block]


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Block