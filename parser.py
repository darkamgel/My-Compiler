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
from errors import ParserError


class Parser:
    """
    Parser:
    Converts tokens into an AST using a context-free grammar.

    TOC link:
    Recursive statement and expression structures are modeled
    with CFG-style parsing.
    """

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
            self.eat("LET")
            name = self.eat("IDENTIFIER").value
            self.eat("ASSIGN")
            expr = self.expression()
            self.eat("SEMICOLON")
            return LetStatement(name, expr)

        if self.current_token.type == "IDENTIFIER":
            name = self.eat("IDENTIFIER").value
            self.eat("ASSIGN")
            expr = self.expression()
            self.eat("SEMICOLON")
            return AssignStatement(name, expr)

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

        raise ParserError(
            f"Invalid statement starting with {self.current_token.type} "
            f"at position {self.current_token.position}"
        )

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

    def expression(self):
        return self.equality()

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
        node = self.factor()
        while self.current_token.type in ("MULTIPLY", "DIVIDE"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        token = self.current_token

        if token.type == "NUMBER":
            self.eat("NUMBER")
            return Number(float(token.value))

        if token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return Variable(token.value)

        if token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expression()
            self.eat("RPAREN")
            return node

        if token.type == "PLUS":
            self.eat("PLUS")
            return UnaryOp("PLUS", self.factor())

        if token.type == "MINUS":
            self.eat("MINUS")
            return UnaryOp("MINUS", self.factor())

        raise ParserError(
            f"Unexpected token {token.type} at position {token.position}"
        )