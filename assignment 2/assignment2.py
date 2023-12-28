#Ryan Behari
#s3618765
#Assignment 2 Interpreter
#Universiteit Leiden
#Assignment 1 code is reused for this assignment#

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
    def __init__(self,description,startPos,endPos):
        super().__init__('illegal character', description,startPos,endPos)

class illegalNumberError(error):
    def __init__(self,description,startPos,endPos):
        super().__init__('disallowed integer', description,startPos,endPos)

class missingExprError(error):
    def __init__(self,description,startPos,endPos):
        super().__init__('missing expression', description,startPos,endPos)

class missingVarError(error):
    def __init__(self,description,startPos,endPos):
        super().__init__('missing variable', description,startPos,endPos)

class missingParenError(error):
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
        # Grammar rules: ⟨expr⟩ ::= ⟨var⟩ | '(' ⟨expr⟩ ')' | '\' ⟨var⟩ ⟨expr⟩ | ⟨expr⟩ ⟨expr⟩ #
        tokens = []
        lastNormalChar = None
        parenthesisOpenAmount = 0
        while(self.currentCharacter != None):
            #Ignore whitespaces and tabs
            if self.currentCharacter in letters:
                #begin of variable found, continue to see if there are more letters or digits 
                newVariable = '' #The construction of the variable name
                while (self.currentCharacter and (self.currentCharacter in letters or self.currentCharacter.isdigit())) and self.currentCharacter != None :
                    newVariable += self.currentCharacter
                    lastNormalChar = self.currentCharacter
                    self.next()
                #No letter or digit found directly after, thus end of variable name
                tokens.append(token(TYPE_VAR,newVariable))
            elif(self.currentCharacter in ' \t\n'):
                #ignore spaces,tabs and newlines
                self.next()
            elif (self.currentCharacter == '('):
                tokens.append(token(TYPE_LEFTPAREN))
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
                parenthesisOpenAmount -= 1
                lastNormalChar = self.currentCharacter
                self.next()
            elif (self.currentCharacter == '\\' or self.currentCharacter == 'λ'):
                tokens.append(token(TYPE_LAMBDA))
                lastNormalChar = self.currentCharacter
                self.next()
                while (self.currentCharacter and self.currentCharacter in ' \t\n'):
                    lastNormalChar = self.currentCharacter
                    self.next()
                if(self.currentCharacter not in letters):
                    startPos = self.position.copyPos()
                    character = '?'
                    return [], missingVarError(character, startPos, self.position)
                    
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

#INTERPRETER#







class Parser:
    def __init__(self, Tokens: token):
        self.Tokens = Tokens
        self.tokenIndex = 0
    
    def parse(self):
        Node = self.expression()
        return Node
    
    def expression(self):
        nextType = self.Tokens[self.tokenIndex].Type
        if(nextType == TYPE_VAR):
            return self.variable()
        elif(nextType == TYPE_LAMBDA):
            return self.function()
        elif(nextType == TYPE_LEFTPAREN):
            return self.application()
        
    def variable(self):
        if(self.tokenIndex < len(self.Tokens)):
            if(self.Tokens[self.tokenIndex].Type == TYPE_VAR):
                self.tokenIndex += 1
                return VarNode(self.Tokens[self.tokenIndex-1])
    
    def function(self):
        if(self.tokenIndex < len(self.Tokens)):
            if(self.Tokens[self.tokenIndex].Type == TYPE_LAMBDA):
                self.tokenIndex += 1
                ourVar = self.variable()
                ourExpr = self.expression()
                return FunctionNode(ourVar, ourExpr)
       
    def application(self):
        if(self.tokenIndex < len(self.Tokens)):
            if(self.Tokens[self.tokenIndex].Type == TYPE_LEFTPAREN):
                self.tokenIndex += 1
                A = self.expression()
                if(self.tokenIndex < len(self.Tokens)):
                    B = self.expression()
                    self.tokenIndex += 1
                    return ApplicationNode(A, B)
    
class FunctionNode:
    def __init__(self,variable, expr):
        self.variable = variable
        self.expr = expr
    
    def __repr__(self):
        return '\\'+str(self.variable)+str(self.expr)
    
    def replace(self, varNode, new, newIndex):
        if (self.expr.replace(varNode,new,newIndex)):
            self.expr = new

    def renameVars(self,index):
        self.expr.renameVars(2*index+2)
        newVar = VarNode(token(TYPE_VAR,self.variable.token.varName, 2*index+2))
        self.replace(VarNode(self.variable.token), newVar, 2*index+2)
        self.variable = newVar

class ApplicationNode():
    def __init__(self, exprA, exprB):
        self.exprA = exprA
        self.exprB = exprB

    def __repr__(self):
        return "("+str(self.exprA)+" "+str(self.exprB)+")"
    
    def replace(self, varNode, new, newIndex):
        NEW = copy.deepcopy(new)
        NEW.renameVariables(newIndex)
        
        if self.exprA.replace(varNode, NEW, 2*newIndex+1):
            self.exprA = NEW
        if self.exprB.replace(varNode, NEW, 2*newIndex+2):
            self.exprB = NEW

    def renameVariables(self, index: FunctionNode):
        self.exprA.renameVariables(2*index+1)
        self.exprB.renameVariables(2*index+2)



    



def readFile(fileName):
    #read the file if it can be found
    try:
        with open(fileName, 'r') as file:
            return file.read()
    except:
        return f'file {fileName} not found'

def run(fileName,text):
    ourlexer = lexer(fileName,text)
    tokensS, errorMess = ourlexer.createTokens()
    return tokensS, errorMess

def main():
    #Check if there is an argument given
    if (len(sys.argv) != 2):
        print("Usage: ./assignment2.py <filename>")
        sys.exit(1)
    else:
        fileContent = readFile(sys.argv[1])

    #run our lexer and collect the tokens and possible errors
    ourResult, ourError = run(sys.argv[1], fileContent)

    if ourError: 
        print(ourError.showError())
        sys.exit(1)
    else: 
        #Print each token in the list
        print('Parsed tokens:', end = ' ')
        print(ourResult)
        P = Parser(ourResult)
        AST = P.parse()
        
        sys.exit(0)

if __name__ == '__main__':
    main()
        
