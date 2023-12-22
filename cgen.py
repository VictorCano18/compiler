from globalTypes import * 
from symtab import *
from Parser import *
import sys
from semantica import *

# Variable global para el offset.
off = 0
# Variable global para almacenar el sp.
sp = 0 
cont = 0

# 'variables' y 'parameters' son arreglos inicializados en 0 donde se 
# va a meter el offset de las variables.
variables = [0] * 25
parameters = [0] * 25
condition = False

# Variable para guardar el nombre de las 
# funciones que se ponen en el codigo de prueba.
funcName = ''

# Función para poder eliminar los nones que tienen algunos
# nodos, ya que a la hora de hacer el parser, no se tomó en cuenta
# este problema (se usó append para ir metiendo los nodos cuando eran)
# más de 2.
def deleteNones(llist):
    return list(filter(None, llist))


def calle(funcName, block):
    # Se cuentan los argumentos 
    args = st_information_lp(funcName, linkedList.head) 
    args = int(len(args))
    # 2 palabras (8) para el return address y el apuntador al old frame
    z = 4*args+8
    print(funcName+':')
    print('move $fp $sp')
    print('sw $ra 0($sp)')
    print('addiu $sp $sp -4')
    cGen(block)
    print('lw $ra 4($sp)')
    print('addiu $sp $sp', z)
    print('lw $fp 0($sp)')
    print('jr $ra')


def caller(args, funcName):
    print('sw $fp 0($sp)')
    print('addiu $sp $sp -4')
    # Se verifica si en los parámetros hay una operación
    for i in (args): 
        if(i.exp == ExpressionType.Op):
            paramToOp_f(i.child[0],i.child[1], i.op)       
        else:
            varEmit(i)   
        print('sw $a0 0($sp)')
        print('addiu $sp $sp -4')
    print('jal', funcName)
   

# Función para poder inicializar los arreglos declarados en el programa ejemplo.
def array_f(id, size):
    global cont
    global sp
    print("addiu $sp $sp -4")
    sp+=4 
    # Se guarda el offset con el cont y posteriormente se aumenta el cont.
    off = 4*cont  
    cont+=1
    st_information_ins(id.val, linkedList.head, off)
    for _ in range(int(size.val)-1):
        print("addiu $sp $sp -4")
        sp+=4
        cont+=1


# Función para declaraciones en los paramateros de las funciones
def param_f(nameParam, n, condition):
    reach = st_scope_lp(n.val, linkedList.head) 
    if condition:
        # Se guarda en nuestro arreglo global parameters en la posicion del scope
        numberOfParams = st_information_lp(nameParam, linkedList.head)   
        maxNumber = (len(numberOfParams) - 1) * 4   
        parameters[int(reach)] = maxNumber
    # Se saca el offset dependiendo la posicion en el arreglo para despues 
    # insertarlo.
    off = parameters[int(reach)] 
    parameters[int(reach)] = parameters[int(reach)] - 4
    st_information_ins(n.val, linkedList.head, off)


# Función para poder declarar variables
def var_f(n):
    global cont
    global sp
    print("addiu $sp $sp -4")
    sp+=4 
    # Se guarda el offset con el cont y posteriormente se aumenta el cont.
    off = 4*cont  
    cont+=1
    st_information_ins(n.val, linkedList.head, off)


# Función para checar el tipo de operador dependiendo de cual se mande como
# parámetro.
def checkOperation(op):
    operatorMat = ''
    if op == TokenType.PLUS:
        operatorMat = 'add'
    elif op == TokenType.MINUS:
        operatorMat = 'sub'
    elif op == TokenType.ASTERISK:
        operatorMat = 'mul'
    elif op == TokenType.SLASH:
        operatorMat = 'div'
    return operatorMat


# Función para detectar las operaciones en las operaciones, dependiendo del operador que nos llegue
# se va  poner al principio de la instrucción '$a0 $t1 $a0' para que sea una comparación
# exitosa.
def paramToOp_f(cgen1, cgen2, op): 
    global sp
    operador = checkOperation(op)
    varEmit(cgen1)
    print('sw $a0 0($sp)')
    print('addiu $sp $sp -4')
    varEmit(cgen2)
    print('lw $t1 4($sp)')
    # En este punto se concatena el operador que nos llegó, ya transformado.
    print(operador,'$a0 $t1 $a0')
    print('addiu $sp $sp 4')


# Función para detectar las operaciones en una asignación, dependiendo del operador que nos llegue
# se va  poner al principio de la instrucción '$a0 $t1 $a0' para que sea una comparación
# exitosa.
def operation_f(var, cgen1, cgen2, op):
    global sp
    operador = checkOperation(op)
    varEmit(cgen1)
    print('sw $a0 0($sp)')
    print('addiu $sp $sp -4')
    varEmit(cgen2)
    print('lw $t1 4($sp)')
    print(operador,'$a0 $t1 $a0')
    print('addiu $sp $sp 4')
    offset = st_information_lp(var.val, linkedList.head)
    reach = st_scope_lp(var.val, linkedList.head)
    # Se agrega esta validación para ver si se están utilizando arreglos para las operaciones
    # y, del mismo modo, verificar si se trata de una variable local o global.
    if(var.child[-1]):
        position = int(var.child[-1].val)
        if int(reach) == 0:
            z =  sp - (offset + 4) * position
            register = '($t5)'
        else:
            z =  (offset + 4) * position + 4
            register = '($fp)'
    else:
        if int(reach) == 0:
            z =  sp - offset 
        
            register = '($t5)'
        else:
            z =  offset + 4
            register = '($fp)'
    print('sw $a0',str(z)+register)


# Funcion para obtener el valor de variables. En caso de que no sea un número, se 
# buscará el registro en la tabla para sacar su valor.
def varEmit(i):  
    if str(i.val).isnumeric():
        print('li $a0', i.val)
    else:
        offset = st_information_lp(i.val, linkedList.head)
        # If para detectar si se trata de una operación.
        if isinstance(offset, list):
            argsN = list(filter(None, i.child[-1].child[-1].child))
            caller(argsN, i.val)
        else:
            reach = st_scope_lp(i.val, linkedList.head)
            # Dependiendo de si se trata de una variable global o local entrará al 
            if int(reach) == 0:
                z =  sp - offset
                register = '($t5)'
            else:
                z =  offset + 4
                register = '($fp)'
            print('lw $a0',str(z)+register)


# Función para determinar si una variable es global o local.
def checkLocalOrGlobal(reach, offset):
    if reach == '0':
        z =  sp - offset
        reg = '($t5)'
    else:
        z =  offset + 4
        reg = '($fp)'
    return reg, z


# Función para verificar que tipo de operador condicional se está mandando y regresar su
# correspondiente para que MIPS lo pueda correr.
def conditionStatement(operator):
    conditional = ''
    if operator == '<':
        conditional = 'blt'
    elif operator == '>':
        conditional = 'bgt'
    elif operator == '<=':
        conditional = 'ble'
    elif operator == '>=':
        conditional = 'bge'
    elif operator == '!=':
        conditional = 'bne'
    elif operator == '==':
        conditional = 'beq'
    return conditional


# Declaraciones internas de funciones 
def arrayFunction_f(id, size, name):
    numberOfParams = st_information_lp(name, linkedList.head)
    if numberOfParams == 'void':
        numberOfParams = ''
    print("addiu $sp $sp -4")
    reach = st_scope_lp(id.val, linkedList.head) 
    offset = 4*(variables[int(reach)] + len(numberOfParams))
    variables[int(reach)] = variables[int(reach)] + 1 
    st_information_ins (id.val, linkedList.head, offset)

    for _ in range(int(size.val)-1):
        print("addiu $sp $sp -4")
        variables[int(reach)] = variables[int(reach)] + 1


# Declaracion de funciones de una variable
def variableFunction_f(i, name):
    numberOfParams = st_information_lp(name, linkedList.head)
    if numberOfParams == 'void':
        numberOfParams = ''
    print("addiu $sp $sp -4")
    reach = st_scope_lp(i.val, linkedList.head) 
    offset = 4*(variables[int(reach)] + len(numberOfParams))
    variables[int(reach)] = variables[int(reach)] + 1 
    st_information_ins(i.val, linkedList.head, offset)


# Función para detectar la operación de una condicional de tipo if.
# Se verifica tanto el lado izquierdo como el derecho de la condición para
# ver si se trata de un arreglo o constate, así como también para saber si
# se trata de una variable local o global.
def if_f(cgen1, cgen2, trueBranch, falseBranch, op):
    condicional = conditionStatement(op)
    if str(cgen1.val).isnumeric():
        varEmit(cgen1)
    else:
        offset = st_information_lp(cgen1.val, linkedList.head)
        reach = st_scope_lp(cgen1.val, linkedList.head)
        if(cgen1.child[-1]):
            position = int(cgen1.child[-1].val)
            if int(reach) == 0:
                z =  sp - (offset + 4) * position
                register = '($t5)'
            else:
                z =  (offset + 4) * position + 4
                register = '($fp)'
        else:
            if int(reach) == 0:
                z =  sp - offset 
                register = '($t5)'
            else:
                z =  offset + 4
                register = '($fp)'
        print('lw $a0',str(z)+register)
    print('sw $a0 0($sp)')
    print('addiu $sp $sp -4')
    if str(cgen2.val).isnumeric():
        varEmit(cgen2)
    else:
        offset = st_information_lp(cgen2.val, linkedList.head)
        reach = st_scope_lp(cgen2.val, linkedList.head)
        if(cgen2.child[-1]):
                position = int(cgen2.child[-1].val)
                if int(reach) == 0:
                    z =  sp - (offset + 4) * position
                    register = '($t5)'
                else:
                    z =  (offset + 4) * position + 4
                    register = '($fp)'
        else:
            if int(reach) == 0:
                z =  sp - offset 
                register = '($t5)'
            else:
                z =  offset + 4
                register = '($fp)'
        print('lw $a0',str(z)+register)
    print('lw $t1 4($sp)')
    print('addiu $sp $sp 4')
    print(condicional,'$t1 $a0 true_branch')
    print('false_branch:')
    cGen(falseBranch)
    print('b end_if')
    print('true_branch:')
    cGen(trueBranch)
    print('end_if:')



# Función para detectar la operación de una condicional de tipo while.
# Se verifica tanto el lado izquierdo como el derecho de la condición para
# ver si se trata de un arreglo o constate, así como también para saber si
# se trata de una variable local o global.
def while_f(cgen1, cgen2, block, op):
    if op == '<':
        op = 'bge'
    elif op == '>':
        op = 'ble'
    elif op == '<=':
        op = 'bgt'
    elif op == '>=':
        op = 'blt'
    elif op == '!=':
        op = 'bne'
    elif op == '==':
        op = 'beq'
    print("while:")
    if str(cgen1.val).isnumeric():
        varEmit(cgen1)
    else:
        offset = st_information_lp(cgen1.val, linkedList.head)
        reach = st_scope_lp(cgen1.val, linkedList.head)
        if(cgen1.child[-1]):
            position = int(cgen1.child[-1].val)
            if int(reach) == 0:
                z =  sp - (offset + 4) * position
                register = '($t5)'
            else:
                z =  (offset + 4) * position + 4
                register = '($fp)'
        else:
            if int(reach) == 0:
                z =  sp - offset 
                register = '($t5)'
            else:
                z =  offset + 4
                register = '($fp)'
        print('lw $a0',str(z)+register)
    print('sw $a0 0($sp)')
    print('addiu $sp $sp -4')
    if str(cgen2.val).isnumeric():
        varEmit(cgen2)
    else:
        offset = st_information_lp(cgen1.val, linkedList.head)
        reach = st_scope_lp(cgen1.val, linkedList.head)
        if(cgen2.child[-1]):
            position = int(cgen2.child[-1].val)
            if int(reach) == 0:
                z =  sp - (offset + 4) * position
                register = '($t5)'
            else:
                z =  (offset + 4) * position + 4
                register = '($fp)'
        else:
            if int(reach) == 0:
                z =  sp - offset 
                register = '($t5)'
            else:
                z =  offset + 4
                register = '($fp)'
        print('lw $a0',str(z)+register)
    print('lw $t1 4($sp)')
    print('addiu $sp $sp 4')
    print(op,'$t1 $a0 end_while')
    cGen(block)
    print("b while")
    print('end_while:')


# Funcion que recursivamente va generando el codigo necesario en lenguaje ensamblador para
# poder compilar el programa de prueba.
def cGen(t):
    global condition
    global funcName
    if (t != None):
        for i in range(len(t.child)):
            if (t.child[i] != None):
                # Se verifica si el nodo es de tipo funcion o si es de tipo declaracion y no tiene ningún
                # segundo hijo el hijo del nodo.
                if(t.exp == ExpressionType.Function or 
                    (t.child[i].exp == ExpressionType.Declaration and t.child[i].child[1] != None)):
                    # Entra solo la primera vez para poder identificar la función main, solo que como MIPS ya detecta
                    # una, se le cambia a new_main.
                    if not condition:
                        condition = True
                        print("move $t5 $sp")
                        print("jal new_main")
                # Se verifica si el nodo es una llamada y si el segundo hijo de su hijo es de tipo argumento.
                if t.child[i].exp == ExpressionType.Call:
                    if t.child[i].child[1].exp == ExpressionType.Args:  
                        # Se obtienen los argumentos, ya que como son lista, se quitan los None con la 
                        # función previamente descrita para despues mandarlo como parametro a nuestra función caller.
                        argsN = deleteNones(t.child[i].child[1].child)
                        args = deleteNones(argsN[0].child)
                        caller(args, t.child[i].child[0].val)
                        # Se marca como 'Check' el nodo para que no se vuelva a visitar de nuevo.
                        t.child[i].exp = ExpressionType.Check
                # Se verifica si es un nodo de tipo grupo.
                elif t.exp == ExpressionType.Group:
                    # Se filtra los nodos del arbol que nos llega para despues recorrerlo con loops de tipo for.
                    listNodes = deleteNones(t.child)
                    # Se verifican los dos hijos del bloque.
                    # Aquí están todas las declaraciones internas del bloque.
                    for node in listNodes[0].child:
                        if node != None:
                            if(node.exp == ExpressionType.Declaration):
                                # Dependiendo si el hijo de la expresión tiene una constante o no,
                                # va a significar si se trata de un arreglo o de una variable normal.
                                if(node.child[-1].exp == ExpressionType.Const):
                                    arrayFunction_f(node.child[-2], node.child[-1], funcName)
                                else:
                                    variableFunction_f(node.child[-1], funcName)
                                node.exp = ExpressionType.Check
                    # Aquí se verifican las asignaciones o los ciclos que puede haber dentro del bloque.
                    for nodeM in listNodes[1].child:
                        if nodeM != None:
                            # Se verifica si el nodo es de tipo asignación
                            if nodeM.exp == ExpressionType.Assign:
                                listNodes = deleteNones(nodeM.child) 
                                # En este punto se verifica si se trata de la asignacion de alguna 
                                # operación o de alguna constante.
                                if listNodes[1].exp == ExpressionType.Op:
                                    if listNodes[1].exp != ExpressionType.Check:
                                        operation_f(listNodes[0], listNodes[1].child[0], listNodes[1].child[1], listNodes[1].op)
                                        listNodes[1].exp = ExpressionType.Check 
                                elif listNodes[1].exp == ExpressionType.Const:
                                    if listNodes[1].exp != ExpressionType.Check:                                        
                                        offset = st_information_lp(listNodes[0].val, linkedList.head)
                                        print('li $t4',listNodes[1].val)
                                        id = listNodes[0].val
                                        reach = st_scope_lp(id, linkedList.head)
                                        if(listNodes[0].child[-1]):
                                            position = int(listNodes[0].child[-1].val)
                                            if int(reach) == 0:
                                                z =  sp - (offset + 4) * position
                                                register = '($t5)'
                                            else:
                                                z =  (offset + 4) * position + 4
                                                register = '($fp)'
                                        else:
                                            if int(reach) == 0:
                                                z =  sp - offset 
                                                register = '($t5)'
                                            else:
                                                z =  offset + 4
                                                register = '($fp)'
                                        print('sw $t4',str(z)+register) 
                                        listNodes[1].exp = ExpressionType.Check
                                # En caso de que se trate de un Id.
                                elif(listNodes[1].exp == ExpressionType.Id 
                                    and listNodes[1].exp != ExpressionType.Check):
                                    # Se hace un for inverso debido a como se guardaron los nodos en el arbol, pero
                                    # se sigue la misma lógica.
                                    for node in range(len(listNodes)-1, -1, -1):
                                        offset = st_information_lp(listNodes[node].val, linkedList.head)
                                        id = listNodes[node].val
                                        reach = st_scope_lp(id, linkedList.head)
                                        if(listNodes[node].child[-1]):
                                            position = int(listNodes[node].child[-1].val)
                                            if int(reach) == 0:
                                                z =  sp - (offset + 4) * position
                                                register = '($t5)'
                                            else:
                                                z =  (offset + 4) * position + 4
                                                register = '($fp)'
                                        else:
                                            if int(reach) == 0:
                                                z =  sp - offset 
                                                register = '($t5)'
                                            else:
                                                z =  offset + 4
                                                register = '($fp)'
                                        if node == 1:
                                            print('lw $a0',str(z)+register) 
                                        else:
                                            print('sw $a0',str(z)+register) 
                                    listNodes[1].exp = ExpressionType.Check
                                # Se verifica si dentro del bloque hay alguna llamada a otra función.
                                elif(listNodes[1].exp == ExpressionType.Call 
                                    and listNodes[1].child[1].exp == ExpressionType.Args):       
                                    argsN = list(filter(None, listNodes[1].child[1].child))
                                    args = list(filter(None, argsN[0].child))              
                                    func_name = listNodes[1].child[0].val 
                                    caller(args, func_name)
                                    listNodes[1].exp = ExpressionType.Check
                            # Se verifica si hay un loop while.
                            elif nodeM.exp== ExpressionType.While:
                                # Se verifica si en uno de los lados de la condicion se trata de un arreglo, o simplemente 
                                # una constante o id.
                                if nodeM.child[-2].child[1] != None:
                                    while_f(nodeM.child[-2].child[0], nodeM.child[-2].child[1], nodeM.child[-1], nodeM.child[-2].op)
                                else:
                                    while_f(nodeM.child[-2].child[0], nodeM.child[-2].child[-1], nodeM.child[-1], nodeM.child[-2].op)
                                nodeM.exp = ExpressionType.Check
                            # Se verifica si hay un loop if.
                            elif nodeM.exp == ExpressionType.If:
                                varComp = deleteNones(nodeM.child[0].child)
                                if_f(varComp[0], varComp[1], nodeM.child[1], nodeM.child[2], nodeM.child[0].op )
                                nodeM.exp = ExpressionType.Check
                            # Se verifica si hay un return en el bloque.
                            elif nodeM.exp == ExpressionType.Return:
                                # Si es solo una constante solo se hace un li de dicha constate.
                                if(nodeM.child[0].exp == ExpressionType.Const):                     
                                    print('li $a0',nodeM.child[0].val)
                                # En caso contrario, se saca el offset y se manda a buscar el valor en la tabla.
                                elif nodeM.child[0].exp == ExpressionType.Id:
                                    offset = st_information_lp(nodeM.child[0].val, linkedList.head)
                                    id = nodeM.child[0].val
                                    reach = st_scope_lp(id, linkedList.head)
                                    if(nodeM.child[0].child[-1]):
                                        position = int(nodeM.child[0].child[-1].val)
                                        if int(reach) == 0:
                                            z =  sp - (offset + 4) * position
                                            register = '($t5)'
                                        else:
                                            z =  (offset + 4) * position + 4
                                            register = '($fp)'
                                    else:
                                        if int(reach) == 0:
                                            z =  sp - offset 
                                            register = '($t5)'
                                        else:
                                            z =  offset + 4
                                            register = '($fp)'
                                    print('lw $a0',str(z)+register)
                                nodeM.exp= ExpressionType.Check
                # Se verifican las declaraciones dentro de los parametros para que solo
                # guarde el offset y no el espacio en stack.
                elif(t.exp != ExpressionType.ParamList and 
                    t.child[i].exp == ExpressionType.Declaration and 
                        t.child[i].child[1] == None and 
                            t.child[i].val != 'void'):                  
                    listNodes = deleteNones(t.child[i].child)             
                    var_f(listNodes[0])
                # Se verifica si es de tipo declaración el nodo, después si se trata de una
                # constante el hijo de este, en caso de que sí, se llama a la funcion de arreglo.
                # En caso contrario se verifica si no se trata del nombre de la funcion 'main'
                # ya que de ser así se la cambiaría el nombre para que no se confunda con la funcion 
                # main del MIPS. 
                # En caso de que no sea main, se mandan los parámetros y luego se llama a la función calle.
                elif t.child[i].exp == ExpressionType.Declaration: 
                    if t.child[i].child[1] != None:
                        if(t.child[i].child[1].exp == ExpressionType.Const):
                            array_f(t.child[i].child[0], t.child[i].child[1])
                        else:
                            name = t.child[i].child[0].val
                            # Se settea la variable global con el nombre.
                            funcName = name
                            if name != "main":
                                listNodes = deleteNones(t.child[i].child[1].child[0].child[-1].child)
                                for j in range(len(listNodes)):
                                    if j == 0:
                                        flag = True
                                    else:
                                        flag = False
                                    param_f(name,listNodes[j].child[0], flag)
                                t.child[i].exp = ExpressionType.Check
                                e = t.child[i].child[1].child[1]
                                calle(name, e)
                            else:
                                print("new_main:")
                cGen(t.child[i])


# Función que se manda a llamar desde main
def codeGen(tree, file):
    global TraceCode
    global code
    stdout = sys.stdout
    sys.stdout = open(file , 'w')
    # Inicio del código ensamblador
    print('.text')
    print('.globl main')
    print('main:')
    print('move $fp $sp')
    cGen(tree)
    sys.stdout.close()
    sys.stdout = stdout




