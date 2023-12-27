#Ryan Behari
#s3618765
#Universiteit Leiden
import sys
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
        tokens = []
        while(self.currentCharacter != None):
            #Ignore whitespaces and tabs
            if self.currentCharacter in letters:
                #begin of variable found, continue to see if there are more letters or digits 
                newVariable = '' #The construction of the variable name
                while (self.currentCharacter and (self.currentCharacter in letters or self.currentCharacter.isdigit())) and self.currentCharacter != None :
                    newVariable += self.currentCharacter
                    self.next()
                #No letter or digit found directly after, thus end of variable name
                tokens.append(token(TYPE_VAR,newVariable))
            elif(self.currentCharacter in ' \t\n'):
                #ignore spaces,tabs and newlines
                self.next()
            elif (self.currentCharacter == '('):
                tokens.append(token(TYPE_LEFTPAREN))
                self.next()
            elif (self.currentCharacter == ')'):
                tokens.append(token(TYPE_RIGHTPAREN))
                self.next()
            elif (self.currentCharacter == '\\' or self.currentCharacter == 'λ'):
                tokens.append(token(TYPE_LAMBDA))
                self.next()
            else:
                startPos = self.position.copyPos()
                illegalChar = self.currentCharacter
                self.next()
                if(illegalChar.isdigit()):
                    #Numbers only allowed in variables after alpha character(s)
                    return [], illegalNumberError(illegalChar, startPos, self.position)
                else:
                    #Other disallowed symbols
                    return [], illegalCharacterError(illegalChar, startPos, self.position)
            
        return tokens, None

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
    '''
    #File support
    #Check if there is an argument given
    if (len(sys.argv) != 2):
        print("Usage: ./assignment1.py <filename>")
        sys.exit(1)
    else:
        fileContent = readFile(sys.argv[1])
    '''

    if(len(sys.argv) >= 2):
        print("No command line arguments allowed")
        sys.exit(1)

    #run our lexer and collect the tokens and possible errors
    text = input('Enter expression: ')
    ourResult, ourError = run('<stdin>', text)

    if ourError: 
        print(ourError.showError())
        sys.exit(1)
    else: 
        #Print each token in the list
        print('Parsed tokens:', end = ' ')
        print(ourResult)
        #Print the simplified expression
        print('Simplified output:', end = ' ')
        for i, token in enumerate(ourResult):
            if token.Type == 'VAR':
                #Leave spaces inbetween variables
                if i + 1 < len(ourResult) and ourResult[i + 1].Type == 'VAR': end = ' '
                else: end = ''
                print(token.Value, end = end)
            elif token.Type == 'LEFTPAREN':
                print('(',end='')
            elif token.Type == 'RIGHTPAREN':
                print(')',end='')
            elif token.Type == 'LAMBDA':
                print('\\',end='')

        sys.exit(0)

if __name__ == '__main__':
    main()
        
