from tokens import Token
from errors import LexerError


class Lexer:
    """
    Lexical analyzer:
    Converts source code into tokens.

    This stage is based on regular languages / finite automata.
    """

    KEYWORDS = {"let", "print"}

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.text):
            return self.text[next_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        # supports // comment
        while self.current_char is not None and self.current_char != "\n":
            self.advance()

    def number(self):
        start_pos = self.pos
        result = ""
        dot_count = 0

        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            if self.current_char == ".":
                dot_count += 1
                if dot_count > 1:
                    raise LexerError(
                        f"Invalid number with multiple dots at position {self.pos}"
                    )
            result += self.current_char
            self.advance()

        return Token("NUMBER", result, start_pos)

    def identifier(self):
        start_pos = self.pos
        result = ""

        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        if result in self.KEYWORDS:
            return Token(result.upper(), result, start_pos)
        return Token("IDENTIFIER", result, start_pos)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "/" and self.peek() == "/":
                self.advance()
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == "+":
                pos = self.pos
                self.advance()
                return Token("PLUS", "+", pos)

            if self.current_char == "-":
                pos = self.pos
                self.advance()
                return Token("MINUS", "-", pos)

            if self.current_char == "*":
                pos = self.pos
                self.advance()
                return Token("MULTIPLY", "*", pos)

            if self.current_char == "/":
                pos = self.pos
                self.advance()
                return Token("DIVIDE", "/", pos)

            if self.current_char == "=":
                pos = self.pos
                self.advance()
                return Token("ASSIGN", "=", pos)

            if self.current_char == "(":
                pos = self.pos
                self.advance()
                return Token("LPAREN", "(", pos)

            if self.current_char == ")":
                pos = self.pos
                self.advance()
                return Token("RPAREN", ")", pos)

            if self.current_char == ";":
                pos = self.pos
                self.advance()
                return Token("SEMICOLON", ";", pos)

            raise LexerError(
                f"Unexpected character '{self.current_char}' at position {self.pos}"
            )

        return Token("EOF", "", self.pos)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == "EOF":
                break
        return tokens