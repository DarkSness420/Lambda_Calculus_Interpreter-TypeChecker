#Ryan Behari
#s3618765
#Assignment 3 Type Checker
#Universiteit Leiden
#Assignment 1+2 code is reused for this assignment#

import sys
import copy

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
uppercaseLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
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

class noOpenParen(error):
    #the judgement expression should be opened with an open parenthese
    def __init__(self,description,startPos,endPos):
        super().__init__('missing expression open parenthese', description,startPos,endPos)

class noLvarError(error):
    #Missing Lvar before a ^ that has been found
    def __init__(self,description,startPos,endPos):
        super().__init__('missing Lvar variable before ^', description,startPos,endPos)

class badUseOfUvarError(error):
    #Missing Uvar should only be used after ^
    def __init__(self,description,startPos,endPos):
        super().__init__('Uvar should only be used after a ^', description,startPos,endPos)


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
TYPE_UVAR = 'UVAR'
TYPE_LVAR = 'LVAR'
TYPE_LEFTPAREN = 'LEFTPAREN'
TYPE_RIGHTPAREN = 'RIGHTPAREN'
TYPE_LAMBDA = 'LAMBDA'
TYPE_OFTYPE = 'OFTYPE' # '^' symbol
TYPE_COLON = 'COLON' # ':' symbol

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
        
#LEXER#
class lexer:

    #Makes tokens from the characters in the text
    #Position is set at -1 because method next will advance
    #it to 0 (first character) to start.
    def __init__(self,fileName,text):
        self.fileName = fileName
        self.text = text
        #start at index and column -1 so we start reading at 0
        self.position = position(-1,0,-1, fileName, text) 
        self.currentCharacter = None
        self.next()

    #Function to read the next character if there is any.
    def next(self):
        self.position.next(self.currentCharacter)
        if (self.position.index < len(self.text)):
            self.currentCharacter = self.text[self.position.index]
        else:
            self.currentCharacter = None

    def createTokens(self):
        # Grammar rules: 
        # ⟨judgement⟩ ::= ⟨expr⟩ ':' ⟨type⟩
        # ⟨expr⟩ ::= ⟨lvar⟩ | '(' ⟨expr⟩ ')' | '\' ⟨lvar⟩ '^' ⟨type⟩ ⟨expr⟩ | ⟨expr⟩ ⟨expr⟩
        # ⟨type⟩ ::= ⟨uvar⟩ | '(' ⟨type⟩ ')' | ⟨type⟩ '->' ⟨type⟩

        tokens = []
        lastNormalChar = None
        lastTokenType = None #If last token appended is LVAR, this is True.
        parenthesisOpenAmount = 0

        while(self.currentCharacter != None or self.currentCharacter in ' \t\n'):
            #Keep going untill we find a normal character
            self.next()

        if(self.currentCharacter != '('):
            #Checks if the expression part of the judgement starts with an open parenthese
            startPos = self.position.copyPos()
            illegalChar = self.currentCharacter
            return [], noOpenParen(illegalChar, startPos, self.position)

        while(self.currentCharacter != None):
            #Ignore whitespaces and tabs
            if self.currentCharacter in lowercaseLetters:
                #begin of Lvar variable found, continue to see if there are more letters or digits 
                newVariable = '' #The construction of the variable name
                while (self.currentCharacter and (self.currentCharacter in letters or self.currentCharacter.isdigit())) and self.currentCharacter != None :
                    newVariable += self.currentCharacter
                    lastNormalChar = self.currentCharacter
                    self.next()
                #No letter or digit found directly after, thus end of Lvar variable name
                tokens.append(token(TYPE_LVAR,newVariable))
                lastTokenType = TYPE_LVAR
            elif(self.currentCharacter in ' \t\n'):
                #ignore spaces,tabs and newlines
                self.next()
            elif (self.currentCharacter == '('):
                tokens.append(token(TYPE_LEFTPAREN))
                lastTokenType = TYPE_LEFTPAREN
                lastNormalChar = self.currentCharacter
                parenthesisOpenAmount += 1
                self.next()       
            elif (self.currentCharacter == ')'):
                #missing expression found
                if(lastNormalChar == '('):
                    startPos = self.position.copyPos()
                    illegalChar = self.currentCharacter
                    return [], missingExprError(illegalChar, startPos, self.position)
                elif (parenthesisOpenAmount == 0):
                    #Missing an opening parenthese somewhere
                    startPos = self.position.copyPos()
                    illegalChar = self.currentCharacter
                    return [], missingParenError(illegalChar, startPos, self.position)
                    
                tokens.append(token(TYPE_RIGHTPAREN))
                lastTokenType = TYPE_RIGHTPAREN
                parenthesisOpenAmount -= 1
                lastNormalChar = self.currentCharacter
                self.next()
            elif (self.currentCharacter == '\\' or self.currentCharacter == 'λ'):
                tokens.append(token(TYPE_LAMBDA))
                lastTokenType = TYPE_LAMBDA
                lastNormalChar = self.currentCharacter
                self.next()
                while (self.currentCharacter and self.currentCharacter in ' \t\n'):
                    lastNormalChar = self.currentCharacter
                    self.next()
                if(self.currentCharacter not in letters):
                    startPos = self.position.copyPos()
                    character = '?'
                    return [], missingVarError(character, startPos, self.position)
            elif (self.currentCharacter == '^'):
                if(lastTokenType != TYPE_LVAR):
                    #If there isnt an Lvar before it, return error
                    startPos = self.position.copyPos()
                    illegalChar = self.currentCharacter
                    return [], noLvarError(illegalChar, startPos, self.position)
                else:
                    tokens.append(token(TYPE_OFTYPE))
                    lastTokenType = TYPE_OFTYPE
                    lastNormalChar = self.currentCharacter
                    self.next()
            elif(self.currentCharacter in uppercaseLetters):
                if(lastTokenType != TYPE_OFTYPE):
                    #Uvar can only be used after ^, so check this
                    startPos = self.position.copyPos()
                    illegalChar = self.currentCharacter
                    return [], badUseOfUvarError(illegalChar, startPos, self.position)
                #begin of Uvar variable found, continue to see if there are more letters or digits 
                newVariable = '' #The construction of the variable name
                while (self.currentCharacter and (self.currentCharacter in letters or self.currentCharacter.isdigit())) and self.currentCharacter != None :
                    newVariable += self.currentCharacter
                    lastNormalChar = self.currentCharacter
                    self.next()
                #No letter or digit found directly after, thus end of Uvar variable name
                tokens.append(token(TYPE_UVAR,newVariable))
                lastTokenType = TYPE_UVAR
            elif(self.currentCharacter == ':'):
                if(lastTokenType != TYPE_RIGHTPAREN):
                    #The expression part should be closed with a close parenthese
                    startPos = self.position.copyPos()
                    illegalChar = self.currentCharacter
                    return [], missingParenError(illegalChar, startPos, self.position)
                else:
                    self.next()
                    while(self.currentCharacter != None or self.currentCharacter in ' \t\n'):
                        #Keep looping untill we find a new character or None
                        self.next()
                    if(self.currentCharacter == None):
                        continue
                    elif(self.currentCharacter != '('):
                         #The type part should either always start with an open parenthese or nothing.
                         startPos = self.position.copyPos()
                         illegalChar = self.currentCharacter
                         return [], missingParenError(illegalChar, startPos, self.position)
                    else:
                        continue


                    



            




                    
            else:
                #Unallowed character found
                startPos = self.position.copyPos()
                illegalChar = self.currentCharacter
                self.next()
                if(illegalChar.isdigit()):
                    #Numbers only allowed in variables after alpha character(s)
                    return [], illegalNumberError(illegalChar, startPos, self.position)
                else:
                    #Other disallowed symbols
                    return [], illegalCharacterError(illegalChar, startPos, self.position)
        if(parenthesisOpenAmount != 0):
            #missing some close parenthesis
            startPos = self.position.copyPos()
            illegalChar = '?'
            return [], missingParenError(illegalChar, startPos, self.position)
            
        return tokens, None