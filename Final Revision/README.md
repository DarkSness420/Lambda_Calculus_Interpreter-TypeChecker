# Lambda calculus: Type Checker
- Ryan Behari
- Leiden University

This program accepts exactly a <u>single</u> argument, namely a text file with a <u>single</u> judgement inside. Enters, tabs and whitespaces(excluding between UVariables and Lvariables) are ignored. The program reads the text from the file into a character string and makes tokens using a modified lexer from the previous assignments that now also excepts Uvariables, Lvariables, ^, -> and Colons as tokens. These tokens are checked if they meet the criteria to get accepted as a judgement, that is, every valuable should have a type. And the judgement is split into an expression part as well as a types part seperated by a colon.

- The program is tested on python 3.10.7 and python 3.10.11 on windows 10.

##### the archived file positives.zip contains several txt documents with example judgements that can be used within the program (and given as an argument)
