# TOC Toy Compiler Project

## Project Title
Design and Implementation of a Toy Compiler Using Regular Languages and Context-Free Grammar

## Overview
This project is a proof-of-concept compiler/interpreter for a small programming language. It demonstrates how Theory of Computation concepts such as regular languages, context-free languages, and computation are used in real compiler construction.

## Supported Features
- variable declaration with `let`
- assignment
- arithmetic expressions
- string literals
- comparison operators
- boolean operators `&&`, `||`, `!`
- `print(...)`
- `input(...)`
- `if / else`
- `while`
- `for`
- comments using `//`
- semantic analysis
- colored terminal output
- AST visualization
- symbol table display

## Theory of Computation Connection

### Regular Languages
The lexer recognizes identifiers, numbers, strings, operators, and punctuation. These token classes are matched in a regular-language style and are closely related to finite automata.

### Context-Free Languages
The parser uses recursive grammar rules for expressions, conditions, and control flow. Nested blocks and recursive expressions are naturally described using context-free grammar.

### Computation
The interpreter executes the abstract syntax tree and maintains a symbol table, demonstrating how formal language definitions become actual computation.

## Example Grammar
```txt
program      -> statement*
statement    -> LET IDENTIFIER ASSIGN expression SEMICOLON
             | IDENTIFIER ASSIGN expression SEMICOLON
             | PRINT LPAREN expression RPAREN SEMICOLON
             | if_statement
             | while_statement
             | for_statement

if_statement -> IF LPAREN expression RPAREN block
             | IF LPAREN expression RPAREN block ELSE block

while_statement -> WHILE LPAREN expression RPAREN block

for_statement -> FOR LPAREN init SEMICOLON expression SEMICOLON update RPAREN block

block        -> LBRACE statement* RBRACE

expression   -> logical_or
logical_or   -> logical_and (OR logical_and)*
logical_and  -> equality (AND equality)*
equality     -> comparison ((EQ | NE) comparison)*
comparison   -> expr ((LT | LE | GT | GE) expr)*
expr         -> term ((PLUS | MINUS) term)*
term         -> unary ((MULTIPLY | DIVIDE) unary)*
unary        -> (PLUS | MINUS | NOT) unary | primary
primary      -> NUMBER
             | STRING
             | IDENTIFIER
             | INPUT LPAREN expression? RPAREN
             | LPAREN expression RPAREN



---

# How to run

From your project folder:

```bash
python main.py sample_program.toy

for trace mode:
python main.py sample_program.toy --trace