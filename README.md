# TOC Toy Compiler Project

## Project Title
Design and Implementation of a Toy Compiler Using Regular Languages and Context-Free Grammar

## Overview
This project is a proof-of-concept compiler/interpreter for a small programming language. It demonstrates how Theory of Computation concepts are used in real applications such as compiler construction.

The language supports:
- variable declaration with `let`
- assignment
- arithmetic expressions
- comparison operators
- `if / else`
- `while`
- print statements
- comments
- block statements with `{}`

## Theory of Computation Relevance

### Regular Languages and Finite Automata
The lexical analysis phase identifies identifiers, keywords, numbers, operators, and punctuation symbols. These token classes can be recognized using regular-language style patterns, which connect directly to finite automata.

### Context-Free Languages
The parser uses recursive grammar rules for expressions, conditions, and block statements. This reflects context-free language theory, especially because nested and recursive structures cannot be handled by finite automata alone.

### Computation
The interpreter executes the abstract syntax tree produced by the parser. This demonstrates how a formal language can be turned into actual computation.

## Example Grammar
```txt
program      -> statement*
statement    -> LET IDENTIFIER ASSIGN expression SEMICOLON
             | IDENTIFIER ASSIGN expression SEMICOLON
             | PRINT LPAREN expression RPAREN SEMICOLON
             | if_statement
             | while_statement

if_statement -> IF LPAREN expression RPAREN block
             | IF LPAREN expression RPAREN block ELSE block

while_statement -> WHILE LPAREN expression RPAREN block

block        -> LBRACE statement* RBRACE

expression   -> equality
equality     -> comparison ((EQ | NE) comparison)*
comparison   -> expr ((LT | LE | GT | GE) expr)*
expr         -> term ((PLUS | MINUS) term)*
term         -> factor ((MULTIPLY | DIVIDE) factor)*
factor       -> NUMBER
             | IDENTIFIER
             | LPAREN expression RPAREN
             | PLUS factor
             | MINUS factor