#Ryan Behari
#s3618765
#Assignment 3 Type Checker
#Universiteit Leiden
#Assignment 1+2 code is reused for this assignment#

import sys
import copy

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

#ERRORS#
class error:
    def __init__(self, name, description, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos
        self.name = name
        self.description = description

    def showError(self):
        message = f'{self.name}: {self.description}'
        message += f'\nfrom {self.startPos.fileName}, line: {self.startPos.lineNum+1}'
        return message
    
class illegalCharacterError(error):
    #Error if and illegal character has been found
    def __init__(self,description,startPos,endPos):
        super().__init__('illegal character', description,startPos,endPos)

class illegalNumberError(error):
    #Error if a number has been found this isn't part of a variable
    def __init__(self,description,startPos,endPos):
        super().__init__('disallowed integer', description,startPos,endPos)

class missingExprError(error):
    #Missing expression after lambda variable
    def __init__(self,description,startPos,endPos):
        super().__init__('missing expression', description,startPos,endPos)

class missingVarError(error):
    #Missing variable after a lambda symbol has been found
    def __init__(self,description,startPos,endPos):
        super().__init__('missing variable', description,startPos,endPos)

class missingParenError(error):
    #There is missing a closed or open parenthese
    def __init__(self,description,startPos,endPos):
        super().__init__('missing a parenthese', description,startPos,endPos)