"""
Lexer implementation for the toy programming language.

This module performs lexical analysis by reading the raw source code
character by character and converting it into a sequence of tokens
that can be used by the parser. It identifies keywords, identifiers,
numbers, strings, operators, punctuation symbols, and comments.

Key responsibilities:
- Skip whitespace and single-line comments
- Recognize language keywords such as let, print, if, else, while, for, and input
- Parse identifiers and numeric literals
- Handle string literals with basic escape sequences
- Detect single-character and multi-character operators
- Raise clear lexical errors for invalid or unexpected input

The lexer acts as the first stage of the compiler/interpreter pipeline:
    Source Code → Lexer → Tokens → Parser

This module helps ensure that the input program is broken into
well-structured token units before syntax analysis begins.
"""

from tokens import Token
from errors import LexerError


class Lexer:
    KEYWORDS = {"let", "print", "if", "else", "while", "for", "input"}

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

    def string(self):
        start_pos = self.pos
        self.advance()  # skip opening quote
        result = ""

        while self.current_char is not None and self.current_char != '"':
            if self.current_char == "\\":
                self.advance()
                if self.current_char is None:
                    raise LexerError(f"Unterminated string at position {start_pos}")
                escapes = {
                    "n": "\n",
                    "t": "\t",
                    '"': '"',
                    "\\": "\\",
                }
                result += escapes.get(self.current_char, self.current_char)
            else:
                result += self.current_char
            self.advance()

        if self.current_char != '"':
            raise LexerError(f"Unterminated string at position {start_pos}")

        self.advance()  # skip closing quote
        return Token("STRING", result, start_pos)

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

            if self.current_char == '"':
                return self.string()

            # two-char operators
            if self.current_char == "=" and self.peek() == "=":
                pos = self.pos
                self.advance()
                self.advance()
                return Token("EQ", "==", pos)

            if self.current_char == "!" and self.peek() == "=":
                pos = self.pos
                self.advance()
                self.advance()
                return Token("NE", "!=", pos)

            if self.current_char == "<" and self.peek() == "=":
                pos = self.pos
                self.advance()
                self.advance()
                return Token("LE", "<=", pos)

            if self.current_char == ">" and self.peek() == "=":
                pos = self.pos
                self.advance()
                self.advance()
                return Token("GE", ">=", pos)

            if self.current_char == "&" and self.peek() == "&":
                pos = self.pos
                self.advance()
                self.advance()
                return Token("AND", "&&", pos)

            if self.current_char == "|" and self.peek() == "|":
                pos = self.pos
                self.advance()
                self.advance()
                return Token("OR", "||", pos)

            # single-char tokens
            single_map = {
                "+": "PLUS",
                "-": "MINUS",
                "*": "MULTIPLY",
                "/": "DIVIDE",
                "=": "ASSIGN",
                "<": "LT",
                ">": "GT",
                "!": "NOT",
                "(": "LPAREN",
                ")": "RPAREN",
                "{": "LBRACE",
                "}": "RBRACE",
                ";": "SEMICOLON",
                ",": "COMMA",
            }

            if self.current_char in single_map:
                pos = self.pos
                ch = self.current_char
                self.advance()
                return Token(single_map[ch], ch, pos)

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