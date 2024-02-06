#######################################
# DIGITS

DIGIT = '0123456789'

######################################

#######################################
# TOKEN TYPES

TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_STAR = 'STAR'
TT_DIVIDE = 'DIVIDE'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'


#####################################

##################################
# ERROR
##################################

class Error:
    def __init__(self, pos_start, pos_end, error, details):
        self.pos_start=pos_start
        self.pos_end=pos_end
        self.error = error
        self.details=details

    def as_string(self):
        result = f"{self.error}:{self.details}"
        result+=f'Filename {self.pos_start.fn}, line{self.pos_start.ln+1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal character', details)

###################################
# POSITION
##################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.ln=ln
        self.col=col
        self.idx=idx
        self.fn=fn
        self.ftxt=ftxt      
    
    def advance(self, curr_char):
        self.idx+=1
        self.col+=1

        if curr_char == '\n':
            self.ln+=1
            self.col=0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


###################################
#TOKEN CLASS
###################################

class Token:
    def __init__(self, type_, value=None):
        self.type=type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        
        return f"{self.type}"
    
####################################
# LEXER
####################################


class Lexer:
    def __init__(self, fn, source):
        self.fn = fn
        self.source = source
        self.pos=Position(-1, 0, -1, fn, source)
        self.curr = None
        self.advance()

    def advance(self):
        self.pos.advance(self.curr)
        self.curr=self.source[self.pos.idx] if self.pos.idx<len(self.source) else None

    def tokenize(self):
        tokens = []

        while self.curr!=None:
            if self.curr in " /t":
                self.advance()
            elif self.curr in DIGIT:
                tokens.append(self.make_number())
            elif self.curr == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.curr == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.curr == '*':
                tokens.append(Token(TT_STAR))
                self.advance()
            elif self.curr == '/':
                tokens.append(Token(TT_DIVIDE))
                self.advance()
            elif self.curr == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.curr == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.curr
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        
        return tokens, None

    def make_number(self):
        dot = 0
        num_str = ''

        while self.curr!=None and self.curr in DIGIT+'.':
            if self.curr == '.':
               if dot==1: break

               dot+=1
               num_str+='.'
            else:
               num_str+=self.curr
                
            self.advance()
        
        if dot==1:
            return Token(TT_FLOAT, float(num_str))
        else:
            return Token(TT_INT, int(num_str)) 

def run(fn, code):
    lexer = Lexer(fn, code)
    tokens, error = lexer.tokenize()
    
    return tokens, error

