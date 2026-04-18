"""
Custom exception classes for different stages of the compiler.

- LexerError: Raised during lexical analysis (tokenization issues).
- ParserError: Raised during syntax analysis (invalid grammar/structure).
- SemanticError: Raised during semantic checks (e.g., undefined variables, type errors).
- InterpreterError: Raised during execution/runtime evaluation.

These help isolate and debug errors at each stage of the compilation pipeline.
"""

class LexerError(Exception):
    pass


class ParserError(Exception):
    pass


class SemanticError(Exception):
    pass


class InterpreterError(Exception):
    pass