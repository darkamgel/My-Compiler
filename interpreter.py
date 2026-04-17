from ast_nodes import (
    Program,
    Block,
    Number,
    Variable,
    BinOp,
    UnaryOp,
    LetStatement,
    AssignStatement,
    PrintStatement,
    IfStatement,
    WhileStatement,
)
from errors import InterpreterError


class Interpreter:
    """
    Executes the AST.

    Includes:
    - optional execution trace
    - symbol table printing
    """

    def __init__(self, trace=False):
        self.symbol_table = {}
        self.trace = trace

    def log(self, message):
        if self.trace:
            print(f"[trace] {message}")

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise InterpreterError(f"No visit method for {type(node).__name__}")

    def visit_Program(self, node: Program):
        self.log("Starting program execution")
        for stmt in node.statements:
            self.visit(stmt)
        self.log("Program execution finished")

    def visit_Block(self, node: Block):
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

        if node.op == "EQ":
            return 1.0 if left == right else 0.0
        if node.op == "NE":
            return 1.0 if left != right else 0.0
        if node.op == "LT":
            return 1.0 if left < right else 0.0
        if node.op == "LE":
            return 1.0 if left <= right else 0.0
        if node.op == "GT":
            return 1.0 if left > right else 0.0
        if node.op == "GE":
            return 1.0 if left >= right else 0.0

        raise InterpreterError(f"Unknown binary operator {node.op}")

    def visit_LetStatement(self, node: LetStatement):
        if node.name in self.symbol_table:
            raise InterpreterError(f"Variable '{node.name}' already declared")
        value = self.visit(node.expr)
        self.symbol_table[node.name] = value
        self.log(f"Declared {node.name} = {self._format_value(value)}")

    def visit_AssignStatement(self, node: AssignStatement):
        if node.name not in self.symbol_table:
            raise InterpreterError(
                f"Variable '{node.name}' must be declared with 'let' first"
            )
        value = self.visit(node.expr)
        self.symbol_table[node.name] = value
        self.log(f"Assigned {node.name} = {self._format_value(value)}")

    def visit_PrintStatement(self, node: PrintStatement):
        value = self.visit(node.expr)
        print(f"→ {self._format_value(value)}")

    def visit_IfStatement(self, node: IfStatement):
        condition_value = self.visit(node.condition)
        self.log(f"IF condition evaluated to {self._format_value(condition_value)}")
        if condition_value != 0:
            self.visit(node.then_branch)
        elif node.else_branch is not None:
            self.visit(node.else_branch)

    def visit_WhileStatement(self, node: WhileStatement):
        iteration = 0
        while self.visit(node.condition) != 0:
            iteration += 1
            self.log(f"WHILE iteration {iteration}")
            self.visit(node.body)

    def _format_value(self, value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def print_symbol_table(self):
        print("===== SYMBOL TABLE =====")
        if not self.symbol_table:
            print("(empty)")
            return

        for name in sorted(self.symbol_table.keys()):
            print(f"{name} = {self._format_value(self.symbol_table[name])}")