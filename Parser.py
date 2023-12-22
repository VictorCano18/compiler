from globalTypes import *
from scanner import *


token = None # holds current token
tokenString = None # holds the token string value
Error = False
#lineno = 1
SintaxTree = None
printsLexer = False
ind = 0


# Se definen los tipos de expresiones que el pareser va a poder identificar
# a lo largo del codigo prueba.
class ExpressionType(Enum): 
    Op = 0
    Const = 1
    Id = 2
    Declaration = 3
    While = 4
    If = 5
    Return = 6
    Else = 7
    Group = 8
    Params = 9
    Function = 10
    Program = 11
    Assign = 12
    ListDeclaration = 13
    ParamList = 14
    Void = 15
    ArgsList = 16
    Args = 17
    Call = 18
    ListStatement = 19
    Check = 20


# Estructura de dato de tipo tree utilizada para poder realizar el AST
class treeNode:
    def __init__(self):
        self.sibling = None
        self.child = [None] * 25
        self.val = None
        self.exp = None
        self.op = None
        self.type = None
        self.lineno = None # SE MODIFICO PARA PODER GUARDAR LA LINEA DE CODIGO


# Función utilizada para mandar los errores del parser.
def syntaxError(message):
    global Error
    print(">>> Syntax error at line " + str(lineno) + ": " + message)#, end='')
    Error = True


# Imprime espacios para poder indentar el arbol final.
def spaces():
    print(' '*ind, end = '')


# Crea nuevos nodos del tipo que se manden en los parametros.
def newNode(tipo):
    t = treeNode()
    if (t == None):
        print("Se terminó la memoria")
    else:
        t.exp = tipo
        t.lineno = lineno
    return t


# Imprime el AST comparando el nodo que le llega por los parametros
# y asi saber de que tipo va a ser el nodo.
def printAST(arbol):
    global ind
    ind += 2
    if arbol != None:
        spaces()
        if arbol.exp == ExpressionType.Op:
            print("Op: ", arbol.op)
        elif arbol.exp == ExpressionType.Const:
            print("Const: ", arbol.val)
        elif arbol.exp == ExpressionType.Id:
            print("ID: ", arbol.val)
        elif arbol.exp == ExpressionType.Declaration:
            print("Declaration: ", arbol.val)
        elif arbol.exp == ExpressionType.Function:
            print("Function: ")
        elif arbol.exp == ExpressionType.Params:
            print("Params: ")
        elif arbol.exp == ExpressionType.Program:
            print("Program: ")
        elif arbol.exp == ExpressionType.Group:
            print("Group: ")
        elif arbol.exp == ExpressionType.If:
            print("If: ")
        elif arbol.exp == ExpressionType.While:
            print("While: ")
        elif arbol.exp == ExpressionType.Return:
            print("Return: ")
        elif arbol.exp == ExpressionType.Assign:
            print("Assign: ", arbol.op)
        elif arbol.exp == ExpressionType.ListDeclaration:
            print("List Declaration: ")
        elif arbol.exp == ExpressionType.ParamList:
            print("Param List: ")
        elif arbol.exp == ExpressionType.Void:
            print("Void")
        elif arbol.exp == ExpressionType.ArgsList:
            print("ArgsList: ")
        elif arbol.exp == ExpressionType.Args:
            print("Args: ")
        elif arbol.exp == ExpressionType.Call:
            print("Call: ")
        elif arbol.exp == ExpressionType.ListStatement:
            print("ListStatement:")
        else:
            print("ExpNode de tipo desconocido")
        # Aquí se mandan cada uno de los nodos a la funcion de imprimir el AST
        for i in range(len(arbol.child)):
            printAST(arbol.child[i])
    ind -= 2


def match(c):
    global token, tokenString, lineno
    if (token == c):
        token, tokenString, lineno = getToken(printsLexer)
    else:
        syntaxError("Unexpected token")


# 1. program -> declaration-list  
def program():
    global token, tokenString, lineno
    t = newNode(ExpressionType.Program)
    while(token!= TokenType.ENDFILE):
        q = declaration_list()
        t.child.append(q)
    return t
    

# 2. declaration-list → declaration {declaration}
def declaration_list():
    d = newNode(ExpressionType.ListDeclaration)
    global token, tokenString, lineno
    if token == TokenType.COMMENT:
        match(TokenType.COMMENT) 
    t = declaration()
    d.child.append(t)
    while (token == TokenType.INT or token == TokenType.VOID):
        t = declaration()
        d.child.append(t)
    return d


# 3. declaration → var-declaration|fun-declaration
def declaration():
    global token, tokenString, lineno    
    t = type_specifier()
    if ((t!=None) and (token == TokenType.ID)):
        p = newNode(ExpressionType.Id)
        p.val = tokenString
        t.child[0] = p
    # else:
    #     syntaxError("Your declaration must have an ID")
    #     token, tokenString, lineno = getToken()  
    match(TokenType.ID)

    if (token == TokenType.OPENPARENTHESIS):
        match(TokenType.OPENPARENTHESIS)
        q = fun_declaration()
        t.child[1] = q
    elif token == TokenType.OPENSQBRACKET:
        q = var_declaration()
        t.child[1] = q
    elif token == TokenType.SEMICOLON:
        match(TokenType.SEMICOLON)
            # else:
            #     syntaxError("Expected ;")
            #     token, tokenString, lineno = getToken()
    else:
        syntaxError("Bad variable declaration")
        token, tokenString, lineno = getToken()
    return t


# 4. var-declaration -> type-specifier ID [ [NUM] ];
def var_declaration():
    global token, tokenString, lineno
    t = None
    if token == TokenType.OPENSQBRACKET:
        match(TokenType.OPENSQBRACKET)
        if token == (TokenType.NUM):
            t = newNode(ExpressionType.Const)
            if ((t!=None) and (token==TokenType.NUM)):
                t.val = int(tokenString)
            if token == TokenType.NUM:
                match(TokenType.NUM)
            else:
                syntaxError("Expected NUM")
                token, tokenString, lineno = getToken()
            if token == TokenType.CLOSESQBRACKET:
                match(TokenType.CLOSESQBRACKET)
            else:
                syntaxError("Expected ]")
                token, tokenString, lineno = getToken()
            if token == TokenType.SEMICOLON:
                match(TokenType.SEMICOLON)
            else:
                syntaxError("Expected ;")
                token, tokenString, lineno = getToken()
        elif token == TokenType.ID:
            syntaxError("The 'id' type is not supported for arrays")
            token, tokenString, lineno = getToken()
            print(token, tokenString, lineno)
        else:
            syntaxError("Bad var declaration")
            token, tokenString, lineno = getToken()
            print(token, tokenString, lineno)
    return t


# 5 type-specifier → int|void
def type_specifier():
    global token, tokenString, lineno
    t = newNode(ExpressionType.Declaration)
    if ((token == TokenType.INT) or (token == TokenType.VOID)):
        t.val = tokenString
        match(token)
    else:
        syntaxError("You must begin with reserved word 'int' or 'void'")
        token, tokenString, lineno = getToken()    
    return t


# 6. fun-declaration → type-specifier ID (params) | compound-stmt
def fun_declaration():
    global token, tokenString, lineno
    t = newNode(ExpressionType.Function)
    if token == (TokenType.CLOSEPARENTHESIS):
        syntaxError("Declaration or 'void' expected in params")
        token, tokenString, lineno = getToken()
    else:
        p = params()
        t.child[0]=p
        match(TokenType.CLOSEPARENTHESIS)
        if token == TokenType.OPENCURLYBRACKET:
            c = compound_stmt()
            t.child[1]=c
        else:
            syntaxError("Expected '{'")
            token, tokenString, lineno = getToken()   
    return t


# 7. params → params-list|void 
def params():
    t = newNode(ExpressionType.Params)
    if token == TokenType.VOID:
        q = newNode(ExpressionType.Declaration)
        q.val = tokenString
        t.child.append(q)
        match(TokenType.VOID)
    else:
        q = param_list()
        t.child.append(q)
    return t


# 8. param-list → param{,param}
def param_list():
    l = newNode(ExpressionType.ParamList)
    t = param()
    l.child.append(t)
    while token!=TokenType.CLOSEPARENTHESIS: 
        match(TokenType.COMMA)
        t = param()
        l.child.append(t)
    return l


# 9. param → type-specifier ID[[]]
def param():
    global token, tokenString, lineno
    t = type_specifier()
    if ((t!=None) and (token==TokenType.ID)):
        p = newNode(ExpressionType.Id)
        p.val = tokenString
        t.child[0] = p
        match(TokenType.ID)
    if token==TokenType.OPENSQBRACKET:
        match(TokenType.OPENSQBRACKET)
        t.child[1] = newNode(ExpressionType.Void)
        match(TokenType.CLOSESQBRACKET)
    return t 


# 10. compound-stmt → {local-declarations statement-list}
def compound_stmt():
    global token, tokenString, lineno
    if token != TokenType.OPENCURLYBRACKET:
        syntaxError("Expected '{' to open the statement")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.OPENCURLYBRACKET)
    t = newNode(ExpressionType.Group)
    while token!=TokenType.CLOSECURLYBRACKET:
        p = local_declations()
        t.child.append(p)
        q = statement_list()
        t.child.append(q)
    if token != TokenType.CLOSECURLYBRACKET:
        syntaxError("Expected '}' to close the statement")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.CLOSECURLYBRACKET)
    return t


# 11. local-declarations → empty{var-declaration}
def local_declations():
    t = None
    x = newNode(ExpressionType.ListDeclaration)
    while (token == TokenType.INT or token == TokenType.VOID):
        t = type_specifier()
        x.child.append(t)
        if ((token==TokenType.ID)):
            p = newNode(ExpressionType.Id)
            p.val = tokenString
            t.child.append(p)
        match(TokenType.ID)
        if(token == TokenType.OPENSQBRACKET):
            q = var_declaration()
            t.child.append(q)
        elif(token == TokenType.SEMICOLON):
            match(TokenType.SEMICOLON)
    return x


# 12. statement-list → empty{statement}
def statement_list():
    t = newNode(ExpressionType.ListStatement)
    while(token == TokenType.ID or token == TokenType.OPENPARENTHESIS or token == TokenType.NUM or token == TokenType.SEMICOLON or
          token == TokenType.OPENCURLYBRACKET or
          token == TokenType.IF or
          token == TokenType.WHILE or
          token == TokenType.RETURN):
          t.child.append(statement())
    if token == TokenType.COMMENT:
        match(TokenType.COMMENT)
    return t


# 13. statement → expression-stmt|compound-stmt|selection-stmt|iteration-stmt|return-stmt
def statement():
    global token, tokenString, lineno
    t = None
    if token == TokenType.ID or token == TokenType.OPENPARENTHESIS or token == TokenType.NUM or token == TokenType.SEMICOLON:
        t = expression_stmt()
    elif token == TokenType.OPENCURLYBRACKET:
        t = compound_stmt()
    elif token == TokenType.IF:
        # print("entro a ifsmt")
        t = selection_stmt()
    elif token == TokenType.WHILE:
        t = iteration_stmt()
    elif token == TokenType.RETURN:
        t = return_stmt()
    return t


# 14. expression-stmt → [expression];
def expression_stmt():
    global token, tokenString, lineno
    t = None
    if (token == TokenType.ID or token == TokenType.OPENPARENTHESIS or token == TokenType.NUM):
        t = expression()
    if token != TokenType.SEMICOLON:
        syntaxError("Expected ';'")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.SEMICOLON)
    return t


# 15. selection-stmt → if(expression) statement [else statement]
def selection_stmt():
    global token, tokenString, lineno
    t = newNode(ExpressionType.If)
    match(TokenType.IF)
    if token != TokenType.OPENPARENTHESIS:
        syntaxError("Expected '(' to open the statement")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.OPENPARENTHESIS)
    if (t!=None):
        t.child[0] = expression()
    if token != TokenType.CLOSEPARENTHESIS:
        syntaxError("Expected ')' to close the statement")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.CLOSEPARENTHESIS)
    if (t!=None):
        t.child[1] = statement()
    if (token==TokenType.ELSE):
        match(TokenType.ELSE)
        if (t!=None):
            t.child[2] = statement()
    return t


# 16. iteration-stmt → while(expression) statement
def iteration_stmt():
    global token, tokenString, lineno
    t = newNode(ExpressionType.While)
    match(TokenType.WHILE)
    if token != TokenType.OPENPARENTHESIS:
        syntaxError("Expected '(' to open the statement")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.OPENPARENTHESIS)
    e = expression() 
    if (t!=None):
        t.child.append(e)
    if token != TokenType.CLOSEPARENTHESIS:
        syntaxError("Expected ')' to close the statement")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.CLOSEPARENTHESIS)
    if (t!=None):
        t.child.append(statement())
    return t


# 17. return-stmt → return[expression];
def return_stmt():
    global token, tokenString, lineno
    t = newNode(ExpressionType.Return)
    match(TokenType.RETURN)
    if (token == TokenType.ID or token == TokenType.OPENPARENTHESIS or token == TokenType.NUM):
        t.child[0] = expression()
    if token != TokenType.SEMICOLON:
        syntaxError("Expected ';'")
        token, tokenString, lineno = getToken()
    else:
        match(TokenType.SEMICOLON)
    return t


# 18. expression → var=expression|simple-expression
def expression():
    global token, tokenString, lineno   
    n = None
    if (token == TokenType.OPENPARENTHESIS):
        o = newNode(ExpressionType.Call)
        n = newNode(o)
        match(TokenType.OPENPARENTHESIS)
        e = expression()
        n.child[0]= e # Duda
        match(TokenType.CLOSEPARENTHESIS)
    elif token == TokenType.ID:
        t = newNode(ExpressionType.Id)
        t.val = tokenString
        match(TokenType.ID)
        if token == TokenType.ASSIGN:
            n = newNode(ExpressionType.Assign)
            n.op = tokenString
            match(TokenType.ASSIGN)
            n.child.append(t)
            n.child.append(expression())
            return n
        elif token == TokenType.OPENSQBRACKET:
            match(TokenType.OPENSQBRACKET)
            p = expression()
            t.child[0] = p
            match(TokenType.CLOSESQBRACKET)
            if token == TokenType.ASSIGN:
                r = newNode(ExpressionType.Assign)
                r.op = tokenString
                match(TokenType.ASSIGN)
                r.child.append(t)
                r.child.append(expression())
                t = r
            elif ((token == TokenType.EQUAL) or (token == TokenType.DIFFERENT) or (token == TokenType.LESSEQUAL)
            or (token == TokenType.GREATEREQUAL) or (token == TokenType.LESS) or (token == TokenType.GREATER)):
                p = newNode(ExpressionType.Op)
                if(p != None):
                    p.child[0] = t
                    p.op = tokenString
                    match(token)
                    t = expression()
                    p.child[1] = t
                    return p
            return t
        elif token == TokenType.OPENPARENTHESIS:
            match(TokenType.OPENPARENTHESIS)
            n = newNode(ExpressionType.Call)
            n.child[0] = t
            a = args()
            n.child[1] = a
            match(TokenType.CLOSEPARENTHESIS)
            return n
        elif ((token == TokenType.EQUAL) or (token == TokenType.DIFFERENT) or (token == TokenType.LESSEQUAL)
            or (token == TokenType.GREATEREQUAL) or (token == TokenType.LESS) or (token == TokenType.GREATER)):
            n = simple_expression()
            n.child[1] = n.child[0]
            n.child[0] = t
            return n
        elif ((token == TokenType.PLUS) or (token == TokenType.MINUS)):
            n = additive_expression()
            n.child[0] = t
            return n
        elif ((token == TokenType.ASTERISK) or (token == TokenType.SLASH)):
            n = term()
            n.child[0] = t
            return n
        n = t   
    elif token == TokenType.NUM:
        n = newNode(ExpressionType.Const)
        if ((n!=None) and (token==TokenType.NUM)):
            n.val = int(tokenString)
            match(TokenType.NUM)
            if((token == TokenType.EQUAL) or (token == TokenType.DIFFERENT) or (token == TokenType.LESSEQUAL)
            or (token == TokenType.GREATEREQUAL) or (token == TokenType.LESS) or (token == TokenType.GREATER)):
                t = simple_expression()
                t.child[1] = t.child[0]
                t.child[0] = n
                return t  
            if ((token == TokenType.PLUS) or (token == TokenType.MINUS)):
                t = additive_expression()
                t.child[0] = n
                n = t  
            if ((token == TokenType.ASTERISK) or (token == TokenType.SLASH)):
                t = term()
                t.child[0] = n
                n = t    
            if((token == TokenType.EQUAL) or (token == TokenType.DIFFERENT) or (token == TokenType.LESSEQUAL)
                or (token == TokenType.GREATEREQUAL) or (token == TokenType.LESS) or (token == TokenType.GREATER)):
                match(token)
                t = expression()
                n = t
        else:
            syntaxError("Bad declaration")
            token, tokenString, lineno = getToken()
    return n


# 19. var -> ID [ [expression] ]
# 20. simple-expression → additive-expression {relop additive-expression} 
# 21. relop → <=|<|>|>=|==|!= 
def simple_expression():
    # t = additive_expression()
    # se compara con relop pero no se si se debe de hacer por aparte la de <= >=?
    t = None
    if((token == TokenType.EQUAL) or (token == TokenType.DIFFERENT) or (token == TokenType.LESSEQUAL)
    or (token == TokenType.GREATEREQUAL) or (token == TokenType.LESS) or (token == TokenType.GREATER)):
        p = newNode(ExpressionType.Op)
        if p != None:
            p.child.append(t)
            p.op = tokenString
            t = p
        match(token)
        if t != None:
            t.child.append(additive_expression())
    return t


# 22. additive-expression → term{addop term}
# 23. addop → +|- 
def additive_expression():
    t = None
    if (token == TokenType.NUM or token == TokenType.ID):
        t = term()
    while((token == TokenType.PLUS) or (token == TokenType.MINUS)):
        p = newNode(ExpressionType.Op)
        if p != None:
            p.child[0] = t
            p.op = token
            t = p
            t.child[1] = term()
    return t


# 24. term → factor{mulop factor}
# 25. mulop → *|/
def term():
    t = None
    if (token == TokenType.NUM or token == TokenType.ID):
        t = factor()
    if ((token == TokenType.PLUS) or (token == TokenType.MINUS)):
        match(token)
        t = factor()
    while((token == TokenType.ASTERISK) or (token == TokenType.SLASH)):
        p = newNode(ExpressionType.Op)
        if p != None:
            p.child[0] = t
            p.op = token
            t = p
            match(token)
            t.child[1] = factor()
    return t


# 26. factor → (expression)|var|call|NUM
def factor():
    global token, tokenString, lineno
    t = None
    if token == TokenType.OPENPARENTHESIS:
        match(TokenType.OPENPARENTHESIS)
        t = expression()
        match(TokenType.CLOSEPARENTHESIS)
    elif token == TokenType.NUM:
        t = newNode(ExpressionType.Const)
        if ((t!=None) and (token==TokenType.NUM)):
            t.val = int(tokenString)
        match(TokenType.NUM)
        return t
    elif (token == TokenType.ID):
        t = newNode(ExpressionType.Id)
        t.val = tokenString
        match(TokenType.ID)
        if(token == TokenType.OPENPARENTHESIS):
            match(TokenType.OPENPARENTHESIS)
            t.child.append(call())
    else:
        syntaxError("Unrecognized expression")
        token, tokenString, lineno = getToken()
    return t


# 27. call → ID(args)
def call():
    p = args()
    match(TokenType.CLOSEPARENTHESIS)
    return p

    
# 28. args → arg-list|empty
def args():
    t = newNode(ExpressionType.Args)
    q = arg_list()
    t.child.append(q)
    return t


# 29. arg-list → expression{, expression}
def arg_list():
    l = newNode(ExpressionType.ArgsList)
    t = expression()
    l.child.append(t)
    while token!=TokenType.CLOSEPARENTHESIS: 
        match(TokenType.COMMA)
        t = expression()
        l.child.append(t)
    return l


def parse(prints = True):
    global token, tokenString, lineno
    token, tokenString, lineno = getToken(printsLexer)
    t = program()
    if (token != TokenType.ENDFILE):
        syntaxError("Code ends before file\n")
    if prints:
        printAST(t)
    return t #, Error

def globales(prog, pos, long): # Recibe los globales del main
    recibeScanner(prog, pos, long) # Para mandar los globales