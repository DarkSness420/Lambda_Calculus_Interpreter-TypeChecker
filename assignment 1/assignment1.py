#Ryan Behari
#s3618765
#Universiteit Leiden

#ERRORS#
class error:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def showError(self):
        return f'{self.name}: {self.description}'
    
class illegalCharacterError(error):
    def __init__(self,description):
        super().__init__('illegal character', description)

class illegalNumberError(error):
    def __init__(self,description):
        super().__init__('disallowed integer', description)

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
    def __init__(self,text):
        self.text = text
        self.position = -1
        self.currentCharacter = None
        self.next()

    #Function to read the next character if there is any.
    def next(self):
        self.position += 1
        if (self.position < len(self.text)):
            self.currentCharacter = self.text[self.position]
        else:
            self.currentCharacter = None

    def createTokens(self):
        tokens = []
        while(self.currentCharacter != None):
            #Ignore whitespaces and tabs
            if self.currentCharacter.isalpha():
                #begin of variable found, continue to see if there are more letters or digits 
                newVariable = '' #The construction of the variable name
                while (self.currentCharacter and (self.currentCharacter.isalpha() or self.currentCharacter.isdigit())) and self.currentCharacter != None :
                    newVariable += self.currentCharacter
                    self.next()
                #No letter or digit found directly after, thus end of variable name
                tokens.append(token(TYPE_VAR,newVariable))
            elif(self.currentCharacter in ' \t'):
                self.next()
            elif (self.currentCharacter == '('):
                tokens.append(token(TYPE_LEFTPAREN))
                self.next()
            elif (self.currentCharacter == ')'):
                tokens.append(token(TYPE_RIGHTPAREN))
                self.next()
            elif (self.currentCharacter == '\\'):
                tokens.append(token(TYPE_LAMBDA))
                self.next()
            else:
                illegalChar = self.currentCharacter
                self.next()
                if(illegalChar.isdigit()):
                    #Numbers only allowed in variables after alpha character(s)
                    return [], illegalNumberError(illegalChar)
                else:
                    #Other disallowed symbols
                    return [], illegalCharacterError(illegalChar)
            
        return tokens, None


def run(text):
    ourlexer = lexer(text)
    tokensS, errorMess = ourlexer.createTokens()
    return tokensS, errorMess

while True:
    textInp = input("inp > ")
    resultaat, ourError = run(textInp)

    if ourError: print(ourError.showError())
    else: print(resultaat)
        
