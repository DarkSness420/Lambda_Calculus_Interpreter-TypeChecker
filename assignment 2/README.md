# Lambda calculus: Interpreter
- Assignment 2, Concepts of programming languages
- Ryan Behari, s3618765
- Universiteit Leiden

This program is technically a continuation of the first assignment, so we will reuse some assets from the first program, namely our lexer/tokenizer and the tokens structure. The program can be run using make run EXPR={filenamewithexpression.txt}. The program takes exactly one argument, namely the text file with a <u>single</u> expression stored in it, the newlines and tabs will be ignored. Just like the predecessor program, this program will read in an expression, but now directly through a given text file and will check for any errors, if the expression is gramatically correct, the program will split parts of the expression into tokens. A new class parser has been implemented to parse these tokens into an abstract syntax tree. In the other newly made class Interpreter, this converted abstract syntax tree will be further simplified if possible with the 3 class nodes, which represents functions, applications and variables. Alpha conversions as well as beta reductions are being used for the simplification. 

- The program is tested on python 3.10.7 and python 3.10.11 on windows 10.

##### A deviation that has been made from the assignment is that some expressions can be simplified into None, that is for example (λx x) since it takes an argument but gives the exact same argument back.

##### the archived file positives.zip contains several txt documents with example expression files that can be used within the program (and given as an argument)
