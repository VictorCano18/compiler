from globalTypes import *

numeroLinea = 1

# Para ir contando el numero de caracteres de cada línea
posicionEnter = 0

def recibeScanner(prog, pos, long): 
    global programa 
    global posicion 
    global progLong
    programa = prog 
    posicion = pos 
    progLong = long 

# Función que recibe el tokenString(token a evaluar) y lo compara
# con base al documento globalTypes en la funcion ReservedWords
# en caso de que coincida, se regresa el tokenType de la palabra 
# reservada, en el otro caso regresa un id.
def palabraReservada(tokenString):
    for w in ReservedWords:
        if tokenString.strip() == w.value:
            return TokenType(tokenString.strip())
    return TokenType.ID

# Función que recibe un texto y linea desde la funcion getToken
# donde: texto = el mensaje de error que se imprime dependiendo
# el token y linea = el numero de linea en la que se encuentra 
# dicho error.
def printError(texto, linea):
    global posicionEnter, posicion
    # Se imprime el numero de línea del error, y el texto de
    # error. Ejemplo: Línea 22: Error caracter no reconocido:
    print("Linea",numeroLinea, ":", texto)
    # Variable de tipo list que, guarda el cada posicion la línea
    # de código, basandose en un .split() de los saltos de línea.
    lineaError = programa.replace('$', '').split('\n')
    # Se imprime la línea del error en cuestión, tomando la 
    # posicion línea que se manda en 
    # los parametros y dependiendo si es un caracter no reconocido
    # o si es un id o int, resta 1 o 2 posiciones.
    print(lineaError[linea])
    if texto == 'Error caracter no reconocido:':
        posicionEnter = posicionEnter - 2
    else:
        posicionEnter = posicionEnter - 1
    # Se imprime el numero de espacios necesarios para que el
    # operador ^ quede justo debajo del error encontrado.
    print(' '*posicionEnter, '^')
    # Una vez que se detectó el error, se le va sumando un 1 a la
    # posicion hasta que encuentre un ; para que los
    # tokens que sigan despues del error, no los marque el programa
    # y no los imprima.
    while(programa[posicion] != ';'):
        posicion+=1
    
# Función para ir imprimiendo los tokens.
def getToken(imprime = True):
    global posicion, numeroLinea, posicionEnter
    tokenString = ""
    currentToken = None
    state = StateType.START
    save = True
    while(state != StateType.DONE):
        # La variable c va a ir recorriendo cada caracter del 
        # programa a escanear.
        c = programa[posicion]
        save = True
        if state == StateType.START:
            # Aquí se va a mover de un estado a otro, dependiendo si
            # es un digito, una letra, un /, un espacio, tab o salto de
            # línea, si es un símbolo especial, o si es algo que no 
            # reconoce el programa.
            if c.isdigit():
                state = StateType.FIRSTNUM
            elif c.isalpha():
                state = StateType.FIRSTID
            elif c == '/':
                state = StateType.FIRSTCOMMENT
            elif ((c == ' ') or (c == '\t') or (c == '\n')):
                # Se va a dejar de guardar el token.
                save = False
                # Sí es un salto de línea, va a resetear la 
                # variable posicionEnter a 0 y se va a aunmentar
                # el numero de línea.
                if (c == '\n'):
                    posicionEnter = 0
                    numeroLinea += 1 # incrementa el número de línea
            # Si no es cualquiera de los estados anteriores, este va a 
            # terminar (DONE), y va a ir verificando a que simbolo especial
            # pertenece. En caso de que concurde con uno de estos, 
            # el token se va a volver del tipo del simbolo espacial. Si no es
            # el caso, entraría al else donde se imprime el error de que
            # no se reconoce el caracter.
            else:
                state = StateType.DONE
                if posicion == progLong: #EOF
                    save = False
                    currentToken = TokenType.ENDFILE
                elif c == "-":
                    currentToken = TokenType.MINUS
                elif c == "*":
                    currentToken = TokenType.ASTERISK
                elif c == "<" and programa[posicion+1] == '=':
                    currentToken = TokenType.LESSEQUAL
                    posicion+=1
                elif c == "<":
                    currentToken = TokenType.LESS
                elif c == ">" and programa[posicion+1] == '=':
                    currentToken = TokenType.GREATEREQUAL
                    posicion+=1
                elif c == ">":
                    currentToken = TokenType.GREATER
                elif c == "!" and programa[posicion+1] == '=':
                    currentToken = TokenType.DIFFERENT
                    posicion+=1
                elif c == '=' and programa[posicion+1] == '=':
                    currentToken = TokenType.EQUAL
                    posicion+=1
                elif c == "=":
                    currentToken = TokenType.ASSIGN
                elif c == "}":
                    currentToken = TokenType.CLOSECURLYBRACKET
                elif c == "{":
                    currentToken = TokenType.OPENCURLYBRACKET
                elif c == "]":
                    currentToken = TokenType.CLOSESQBRACKET
                elif c == "[":
                    currentToken = TokenType.OPENSQBRACKET
                elif c == ")":
                    currentToken = TokenType.CLOSEPARENTHESIS
                elif c == "(":
                    currentToken = TokenType.OPENPARENTHESIS
                elif c == ",":
                    currentToken = TokenType.COMMA
                elif c == ";":
                    currentToken = TokenType.SEMICOLON
                elif c == "+":
                    currentToken = TokenType.PLUS
                else:
                    currentToken = TokenType.ERROR
                    printError("Error caracter no reconocido:", numeroLinea-1)

        ######
        # ID #
        ######

        # Cuando se detecte que el token es una letra, entra a esta
        # condición.
        elif state == StateType.FIRSTID:
            # Si el siguiente token sigue siendo una letra, se queda
            # en este mismo estado.
            if c.isalpha():
                state = StateType.FIRSTID
            # Esta serie de condiciones es por si en el codigo a escanear
            # contiene antes o depués paréntesis, corchetes, llaves, 
            # operadores matemáticos, comas, !, = o, saltos de línea, tabs
            # u espacios. Ya que si no, una letra que esté así: void(main)
            # lo detectaría como error.
            elif ((c == ' ') or (c == '\t') or (c == '\n') or (c == ';')
                or (c == '}') or (c == ')') or (c == ']') or (c == '=') 
                or (c == '!') or (c == ',') or (c == '(') or (c == '[')
                or (c == '{') or (c == '*') or (c == '+') or (c == '-')
                or (c == '/') or (c == '<') or (c == '>') or (c == '<=')
                or (c == '>=') or (c == '==') or (c == '!=')):
                if posicion <= progLong:
                    posicion -= 1 # ungetNextChar()
                    posicionEnter -= 1
                # Se deja de guardar el token.
                save = False
                # El estado termina (DONE)
                state = StateType.DONE
                # El token actual ahora es de tipo ID.
                currentToken = TokenType.ID
            # En caso de que no sea una letra y no cumpla con las
            # condiciones de arriba, el estado terminará pero el token
            # será de tipo error.
            else:
                if posicion <= progLong:
                    posicion -= 1 # ungetNextChar()
                    posicionEnter -= 1
                # Se deja de guardar el token.
                save = False
                # El estado termina (DONE)
                state = StateType.DONE
                # El token actual ahora es de tipo ERROR.
                currentToken = TokenType.ERROR
                # Mandamos a llamar a nuestra función de error con el 
                # texto y linea en los parametros.
                printError("Error en la formacion de un ID:", numeroLinea-1)

        #######
        # INT #
        #######

        # Cuando se detecte que el token es un número, entra a esta
        # condición.
        elif state == StateType.FIRSTNUM:
            # Si el siguiente token sigue siendo un número, se queda
            # en este mismo estado.
            if c.isdigit():
                state = StateType.FIRSTNUM
            # Esta serie de condiciones es por si en el codigo a escanear
            # contiene antes o depués paréntesis, corchetes, llaves, 
            # operadores matemáticos, comas, !, = o, saltos de línea, tabs
            # u espacios. Ya que si no, un número que esté así: 1+1
            # lo detectaría como error.
            elif ((c == ' ') or (c == '\t') or (c == '\n') or (c == ';')
                or (c == '}') or (c == ')') or (c == ']') or (c == '=') 
                or (c == '!') or (c == ',') or (c == '(') or (c == '[')
                or (c == '{') or (c == '*') or (c == '+') or (c == '-')
                or (c == '/')):
                if posicion <= progLong:
                    posicion -= 1 # ungetNextChar()
                    posicionEnter -= 1
                # Se deja de guardar el token.
                save = False
                # El estado termina (DONE)
                state = StateType.DONE
                # El token actual ahora es de tipo NUM.
                currentToken = TokenType.NUM
            # condiciones de arriba, el estado terminará pero el token
            # será de tipo error.
            else:
                if posicion <= progLong:
                    posicion -= 1 # ungetNextChar()
                    posicionEnter -= 1
                # Se deja de guardar el token.
                save = False
                # El estado termina (DONE)
                state = StateType.DONE
                # El token actual ahora es de tipo ERROR.
                currentToken = TokenType.ERROR
                # Mandamos a llamar a nuestra función de error con el 
                # texto y linea en los parametros.
                printError("Error en la formacion de un INT:", numeroLinea-1)

        ###########
        # COMMENT #
        ###########

        # Cuando anteriormente se detectó un slash, se vendrá a este estado
        # para checar si es un comentario, o simplemente un símbolo especial.
        elif state == StateType.FIRSTCOMMENT:
            # En caso de que sea un asterisco, se irá al siguiente estado ya
            # que sí es un comentario.
            if c == '*':
                state = StateType.SECONDCOMMENT
            # En caso contrario, el estado terminará y será reconocido como un
            # slash.
            else:
                if posicion <= progLong:
                    posicion -= 1 # ungetNextChar()
                    posicionEnter -= 1
                # Se deja de guardar el token.
                save = False
                # El estado termina (DONE)
                state = StateType.DONE
                # El token actual ahora es de tipo SLASH.
                currentToken = TokenType.SLASH

        # En este estado se van a ir guardando los caracteres del comentario
        # o, en caso de que termine el comentario se va a detectar.
        elif state == StateType.SECONDCOMMENT:
            # Si el caracter actual, y el siguiente son */ consecutivamente
            # significa que es el cierre del comentario, por lo tanto, el 
            # estado terminaria y el token será de tipo comentario.
            if c == '*' and programa[posicion+1] == '/':
                if posicion <= progLong:
                    posicion += 1 # ungetNextChar()
                    posicionEnter -= 1
                # Se deja de guardar el token.
                save = False
                # El estado termina (DONE)
                state = StateType.DONE
                # El token actual ahora es de tipo COMMENT.
                currentToken = TokenType.COMMENT 
            # Si no se trata de un cierre de comentario, se irá a este mismo estado
            # ya que se trata de un comentario. Si hay un salto de línea, se va a incrementar
            # en 1 la variable numeroLinea.           
            else:
                if c == "\n":
                    numeroLinea += 1
                state = StateType.SECONDCOMMENT
        

        # En caso de que el estado termine (DONE) 
        elif state == StateType.DONE:
            None
        # Si es otro tipo de error, que no se detectan arriba
        # entra a aquí, e imprime el estado y el token se vuelve
        # de tipo error.
        else:
            print('Scanner Bug: state= '+str(state))
            state = StateType.DONE
            currentToken = TokenType.ERROR
        # Condicion para poder ir concatenando nuestro token.
        if save:
            # Si el token actual es un símbolo espacial de 2 caracteres, se le va a concatenar 
            # el caracter y el caracter + 1.
            if ((currentToken == TokenType.GREATEREQUAL) or (currentToken == TokenType.LESSEQUAL)
            or (currentToken == TokenType.DIFFERENT) or (currentToken == TokenType.EQUAL)):
                tokenString = tokenString + c + programa[posicion]
            else:
                tokenString = tokenString + c
        # Una vez que el estado es DONE, se verifica si el token es
        # de tipo id, si es el caso, currentToken se iguala a lo que 
        # regresa nuestra funcion palabraReservada mandándole como
        # parámetro la palabra que formamos.
        if state == StateType.DONE:
            if currentToken == TokenType.ID:
                currentToken = palabraReservada(tokenString)  
        # La variable global de posicion se incrementa para que cambie
        # al siguiente caracter del token en cuestión.          
        posicion += 1
        # Se incrementa esta variable para ir guardando el número 
        # de caracteres de cada línea.
        posicionEnter += 1
    if imprime:
        # Se imprime token por token a menos que este sea de tipo error.
        if currentToken != TokenType.ERROR:
            print(numeroLinea, currentToken," = ", tokenString) # prints a token and its lexeme
    return currentToken, tokenString, numeroLinea