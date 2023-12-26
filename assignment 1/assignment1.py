#Ryan Behari
#s3618765
#Universiteit Leiden

class token:
    #This function is for creating a new token
    def __init__(self, Type, Value):
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

