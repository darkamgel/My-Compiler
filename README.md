# TOC Toy Compiler Project

## Project Title
Design and Implementation of a Toy Compiler Using Regular Languages and Context-Free Grammar

## Overview
This project is a proof-of-concept compiler/interpreter designed to demonstrate how Theory of Computation is used in real applications. The compiler supports a small programming language with variable declarations, assignment statements, arithmetic expressions, and print statements.

## Theory of Computation Relevance

### 1. Regular Languages and Finite Automata
The lexical analysis stage of the compiler is based on regular-language style token recognition. Tokens such as identifiers, keywords, numbers, operators, and punctuation symbols can be described by regular patterns. This makes finite automata the theoretical foundation of the lexer.

### 2. Context-Free Languages
The parser is based on context-free grammar. Arithmetic expressions and statement structures are recursive, especially with nested parentheses. Such structures are naturally modeled using context-free grammar rather than finite automata.

### 3. Computation
After lexical analysis and parsing, the interpreter executes the abstract syntax tree. This shows how theoretical language rules can be transformed into actual computation.

## Supported Language Features
- `let x = expression;`
- `x = expression;`
- `print(expression);`
- arithmetic operators: `+`, `-`, `*`, `/`
- parentheses
- comments using `//`

## Example Program
```toy
let x = 10 + 20;
let y = x * 3;
print(y);