from ast_nodes import (
    Program,
    Number,
    Variable,
    BinOp,
    UnaryOp,
    LetStatement,
    AssignStatement,
    PrintStatement,
)
from errors import InterpreterError


class Interpreter:
    """
    Executes the AST.
    """

    def __init__(self):
        self.symbol_table = {}

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise InterpreterError(f"No visit method for {type(node).__name__}")

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Number(self, node: Number):
        return node.value

    def visit_Variable(self, node: Variable):
        if node.name not in self.symbol_table:
            raise InterpreterError(f"Undefined variable '{node.name}'")
        return self.symbol_table[node.name]

    def visit_UnaryOp(self, node: UnaryOp):
        value = self.visit(node.operand)
        if node.op == "PLUS":
            return +value
        if node.op == "MINUS":
            return -value
        raise InterpreterError(f"Unknown unary operator {node.op}")

    def visit_BinOp(self, node: BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == "PLUS":
            return left + right
        if node.op == "MINUS":
            return left - right
        if node.op == "MULTIPLY":
            return left * right
        if node.op == "DIVIDE":
            if right == 0:
                raise InterpreterError("Division by zero")
            return left / right

        raise InterpreterError(f"Unknown binary operator {node.op}")

    def visit_LetStatement(self, node: LetStatement):
        if node.name in self.symbol_table:
            raise InterpreterError(
                f"Variable '{node.name}' already declared"
            )
        self.symbol_table[node.name] = self.visit(node.expr)

    def visit_AssignStatement(self, node: AssignStatement):
        if node.name not in self.symbol_table:
            raise InterpreterError(
                f"Variable '{node.name}' must be declared with 'let' first"
            )
        self.symbol_table[node.name] = self.visit(node.expr)

    def visit_PrintStatement(self, node: PrintStatement):
        value = self.visit(node.expr)
        if isinstance(value, float) and value.is_integer():
            print(int(value))
        else:
            print(value)