"""
Parser implementation for the toy programming language.

This module performs syntax analysis by taking the token stream
produced by the lexer and converting it into an Abstract Syntax Tree (AST).
The AST represents the hierarchical structure of the source program
and is later used for semantic analysis and interpretation.

Main responsibilities:
- Parse complete programs into statement lists
- Recognize variable declarations and assignments
- Parse print statements and input expressions
- Handle control flow structures such as if, while, and for
- Build expression trees with correct operator precedence
- Support arithmetic, comparison, logical, and unary operators
- Raise clear syntax errors when invalid token sequences are found

The parser uses a recursive descent approach, where each method
handles a specific grammar rule such as statements, expressions,
blocks, or primary values.

Overall, this module acts as the bridge between raw tokens
and structured program representation:
    Tokens → Parser → AST
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
from errors import ParserError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        raise ParserError(
            f"Expected {token_type}, got {self.current_token.type} "
            f"at position {self.current_token.position}"
        )

    def parse(self):
        statements = []
        while self.current_token.type != "EOF":
            statements.append(self.statement())
        self.eat("EOF")
        return Program(statements)

    def statement(self):
        if self.current_token.type == "LET":
            stmt = self.let_statement()
            self.eat("SEMICOLON")
            return stmt

        if self.current_token.type == "IDENTIFIER":
            stmt = self.assign_statement()
            self.eat("SEMICOLON")
            return stmt

        if self.current_token.type == "PRINT":
            self.eat("PRINT")
            self.eat("LPAREN")
            expr = self.expression()
            self.eat("RPAREN")
            self.eat("SEMICOLON")
            return PrintStatement(expr)

        if self.current_token.type == "IF":
            return self.if_statement()

        if self.current_token.type == "WHILE":
            return self.while_statement()

        if self.current_token.type == "FOR":
            return self.for_statement()

        raise ParserError(
            f"Invalid statement starting with {self.current_token.type} "
            f"at position {self.current_token.position}"
        )

    def let_statement(self):
        self.eat("LET")
        name = self.eat("IDENTIFIER").value
        self.eat("ASSIGN")
        expr = self.expression()
        return LetStatement(name, expr)

    def assign_statement(self):
        name = self.eat("IDENTIFIER").value
        self.eat("ASSIGN")
        expr = self.expression()
        return AssignStatement(name, expr)

    def block(self):
        self.eat("LBRACE")
        statements = []
        while self.current_token.type != "RBRACE":
            statements.append(self.statement())
        self.eat("RBRACE")
        return Block(statements)

    def if_statement(self):
        self.eat("IF")
        self.eat("LPAREN")
        condition = self.expression()
        self.eat("RPAREN")
        then_branch = self.block()

        else_branch = None
        if self.current_token.type == "ELSE":
            self.eat("ELSE")
            else_branch = self.block()

        return IfStatement(condition, then_branch, else_branch)

    def while_statement(self):
        self.eat("WHILE")
        self.eat("LPAREN")
        condition = self.expression()
        self.eat("RPAREN")
        body = self.block()
        return WhileStatement(condition, body)

    def for_statement(self):
        self.eat("FOR")
        self.eat("LPAREN")

        if self.current_token.type == "LET":
            init = self.let_statement()
        else:
            init = self.assign_statement()
        self.eat("SEMICOLON")

        condition = self.expression()
        self.eat("SEMICOLON")

        update = self.assign_statement()
        self.eat("RPAREN")

        body = self.block()
        return ForStatement(init, condition, update, body)

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == "OR":
            op = self.current_token.type
            self.eat("OR")
            node = BinOp(node, op, self.logical_and())
        return node

    def logical_and(self):
        node = self.equality()
        while self.current_token.type == "AND":
            op = self.current_token.type
            self.eat("AND")
            node = BinOp(node, op, self.equality())
        return node

    def equality(self):
        node = self.comparison()
        while self.current_token.type in ("EQ", "NE"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.comparison())
        return node

    def comparison(self):
        node = self.expr()
        while self.current_token.type in ("LT", "LE", "GT", "GE"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.expr())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in ("PLUS", "MINUS"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.term())
        return node

    def term(self):
        node = self.unary()
        while self.current_token.type in ("MULTIPLY", "DIVIDE"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.unary())
        return node

    def unary(self):
        token = self.current_token
        if token.type in ("PLUS", "MINUS", "NOT"):
            self.eat(token.type)
            return UnaryOp(token.type, self.unary())
        return self.primary()

    def primary(self):
        token = self.current_token

        if token.type == "NUMBER":
            self.eat("NUMBER")
            return Number(float(token.value))

        if token.type == "STRING":
            self.eat("STRING")
            return String(token.value)

        if token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return Variable(token.value)

        if token.type == "INPUT":
            self.eat("INPUT")
            self.eat("LPAREN")
            prompt = None
            if self.current_token.type != "RPAREN":
                prompt = self.expression()
            self.eat("RPAREN")
            return InputExpression(prompt)

        if token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expression()
            self.eat("RPAREN")
            return node

        raise ParserError(
            f"Unexpected token {token.type} at position {token.position}"
        )