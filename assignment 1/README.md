# Lambda calculus: syntax
- Assignment 1, Concepts of programming languages
- Ryan Behari, s3618765
- Universiteit Leiden

This program can be run by using "make run" in this directory. or just by simply running 
python assignment1.py . The user can enter one expression into the terminal, and this
expression will be read and split into tokens using a lexer/tokenizer. If the expression
is grammatically correct according to lambda calculus, the parsed tokens will be displayed
and the screen as well as a minimalistic output of the original expression. If there are any
errors found in the program, this will be displayed instead and the program exits with code 1.
There are no defects or any deviations from the assignment. 

- The program is tested on python 3.10.7 and python 3.10.11 on windows 10.

##### It is possible to use a file with a <u>single</u> expression in it, and give that to the program to use as stdin newlines, tabs and unnecesary whitepaces (that is, any whitespaces that arent between variables) are ignored.

##### the archived file positives.zip contains several txt documents with example expressions that can be used within the program


