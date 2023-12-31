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

#POSITION#
class position:
    def __init__(self,index,lineNum,colomNum, fileName, fileText):
        self.index = index
        self.lineNum = lineNum
        self.colomNum = colomNum
        self.fileName = fileName
        self.fileText = fileText
        
    
    def next(self, currentCharacter):
        self.colomNum += 1
        self.index += 1
        #check if newline character is found
        if(currentCharacter == '\n'):
            #since we start on a new line, the first word is again at column 0
            self.lineNum += 1
            self.colomNum = 0
        return self
    
    def copyPos(self):
        #returns this object
        return position(self.index,self.lineNum,self.colomNum,self.fileName,self.fileText)

#TOKENS#
TYPE_VAR = 'VAR'
TYPE_LEFTPAREN = 'LEFTPAREN'
TYPE_RIGHTPAREN = 'RIGHTPAREN'
TYPE_LAMBDA = 'LAMBDA'

class token:
    #This function is for creating a new token
    def __init__(self, Type, Value = None):
        self.Type = Type
        self.Value = Value
        self.internIndex = 0

    #Function to represent the token for display
    def __repr__(self):
        #if the token has a value, print type and then the value
        #if it doesn't have one, just print the type.
        if (self.Value):
            return f'{self.Type}:{self.Value}'
        else:
            return f'{self.Type}'