from enum import Enum

# TOKENTYPE
class TokenType(Enum):
    ENDFILE = 300
    ERROR = 401
    COMMENT = 500
    VAR = 200
    FUNCTION = 250
    EMPTY = None
    PARAMS = 120
    # RESERVED WORDS
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    # MULTICHARACTER TOKENS
    ID = 111
    NUM = 000
    # SPECIAL SYMBOLS
    ASSIGN = '=='
    EQUAL = '='
    PLUS = '+'
    MINUS = '-'
    ASTERISK = '*'
    SLASH = '/'
    DIFFERENT = '!='
    LESS = '<'
    LESSEQUAL = '<='
    GREATER = '>'
    GREATEREQUAL = '>='
    OPENPARENTHESIS = '('
    CLOSEPARENTHESIS = ')'
    OPENSQBRACKET = '['
    CLOSESQBRACKET = ']'
    OPENCURLYBRACKET = '{'
    CLOSECURLYBRACKET = '}'
    COMMA = ','
    SEMICOLON = ';'


# STATETYPE
class StateType(Enum):
    START = 0
    FIRSTID = 1
    FIRSTNUM = 2
    FIRSTCOMMENT = 3
    SECONDCOMMENT = 4
    DONE = 5

# RESERVED WORDS
class ReservedWords(Enum):
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'