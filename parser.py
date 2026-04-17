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
from errors import ParserError


class Parser:
    """
    Parser:
    Converts tokens into an AST using a context-free grammar.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None

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
        """
        statement ->
              LET IDENTIFIER ASSIGN expr SEMICOLON
            | IDENTIFIER ASSIGN expr SEMICOLON
            | PRINT LPAREN expr RPAREN SEMICOLON
        """
        if self.current_token.type == "LET":
            self.eat("LET")
            name = self.eat("IDENTIFIER").value
            self.eat("ASSIGN")
            expr = self.expr()
            self.eat("SEMICOLON")
            return LetStatement(name, expr)

        if self.current_token.type == "IDENTIFIER":
            name = self.eat("IDENTIFIER").value
            self.eat("ASSIGN")
            expr = self.expr()
            self.eat("SEMICOLON")
            return AssignStatement(name, expr)

        if self.current_token.type == "PRINT":
            self.eat("PRINT")
            self.eat("LPAREN")
            expr = self.expr()
            self.eat("RPAREN")
            self.eat("SEMICOLON")
            return PrintStatement(expr)

        raise ParserError(
            f"Invalid statement starting with {self.current_token.type} "
            f"at position {self.current_token.position}"
        )

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
            node = self.expr()
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