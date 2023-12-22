########################################################
#                                                      #
#                                                      #
# Para este código se usó la double linked list tomado #
# de referencia de la página:                          #
# https://www.geeksforgeeks.org/doubly-linked-list/ el #
# 11 de Mayo del 2022                                  #
#                                                      #
#                                                      #
########################################################

from symtab import * 
from Parser import *
from symtable import *
from globalTypes import *

# Esta parte es el código de referencia para la Double Linked List
class Node:
    def __init__(self, next=None, prev=None, data=None, name=None, scope=None):
        self.next = next # reference to next node in DLL
        self.prev = prev # reference to previous node in DLL
        self.data = data
        self.name = name
        self.scope = scope
    
class DoublyLinkedList:
    # Constructor for empty Doubly Linked List
    def __init__(self):
        self.head = None
    # Given a reference to the head of a list and an
    # integer, inserts a new node on the front of list
    def push(self, name, data, scope):
        # 1. Allocates node
        # 2. Put the data in it
        new_node = Node()

        # print(data)
        new_node.name = name
        new_node.data = data
        new_node.scope = scope
 
        # 3. Make next of new node as head and
        # previous as None (already None)
        new_node.next = self.head
 
        # 4. change prev of head node to new_node
        if self.head is not None:
            self.head.prev = new_node
 
        # 5. move the head to point to the new node
        self.head = new_node

    def printList(self, node):
        print("\nTraversal in forward direction")
        while node:
            print(" {}".format(node.data))
            last = node
            node = node.next

        print("\nTraversal in reverse direction")
        while last:
            print(" {}".format(last.data))
            last = last.prev   

# Aquí se inicializa una lista doblemente ligada para poder almacenar todos los nodos.
global linkedList 
linkedList = DoublyLinkedList()

def traverse(t, preProc, postProc):
    if (t != None):
        preProc(t)
        for i in range(len(t.child)):
            traverse(t.child[i],preProc,postProc)
        postProc(t)

def nullProc(t):
    None

# Aquí se imprimen todos los errores que detecta el analizador semántico
def typeError(t, message, token):
    # Se vuelve a abrir el archivo de texto para recuperar el programa completo
    f = open('prueba.txt', 'r')
    programa = f.read()
    p = programa.splitlines()
    # Se imprime el mensaje en la línea correspondiente
    print("Type error at line", t.lineno, ":",message)
    # Se marca el lugar donde aparece el error
    print(p[t.lineno-1])
    pos = p[t.lineno-1].find(str(token))
    print(''.rjust(pos), end='')
    print('^')

# Aquí se checa cada nodo que se genera, en donde, dependiendo de la expresión, 
# se entra a una condicional. Si al final se cumple con todas las condiciones,
# entra al error que genera la semántica.
def checkNode(t):
    global linkedList
    temp = ''
    if t.exp == ExpressionType.Assign:
        n = list(filter(None, t.child))
        if (st_lookup_general(n[0].val, linkedList, 0) == -1):
            typeError(t,"The variable is not declared", n[0].val)
    elif t.exp == ExpressionType.Op:
        filtered_list = list(filter(None, t.child))
        size = len(filtered_list)
        for i in range(size):
            if str(filtered_list[i].val).isnumeric() != True:
                if st_lookup_general(filtered_list[i].val, linkedList, 0) != 'int':
                    typeError(t,"Operation applied to non-integer", filtered_list[i].val)
    elif t.exp == ExpressionType.Declaration:
        temp = t.val
        if t.child[1]:
            if t.child[1].exp == ExpressionType.Function:
                group = t.child[1].child[1]
                if group.exp == ExpressionType.Group:
                    listStatement = group.child[-1]
                    if listStatement.exp == ExpressionType.ListStatement:
                        returnVar = listStatement.child[-1]
                        if returnVar.exp == ExpressionType.Return:
                            checkVar = returnVar.child[0]
                            if checkVar and checkVar.val != None:
                                if temp != st_lookup_general(checkVar.val, linkedList, 0):
                                    typeError(t,"The fuction is not declare as 'int'", returnVar.child[0])
                            else:
                                if temp != 'void':
                                    typeError(t,"The fuction is not declare as 'void'", checkVar)
                        # elif temp != 'void': 
                        #     typeError(t,"The function without return statement", returnVar.child[0])
                        
    elif t.exp == ExpressionType.Call:
        function_name = t.child[0].val
        if function_name != 'input' and function_name != 'output':
            if (st_lookup_general(function_name, linkedList, 0) == -1):
                typeError(t,"The function is not declared", function_name)
            else:
                params = st_lookup_general(function_name,linkedList,2)
                n = list(filter(None, t.child[1].child[-1].child))
                size = len(n)
                if size == 0 and params != 'void':
                    typeError(t,"The function does not receive any argument", function_name)
                else:
                    for i in range(len(n)):
                        if str(n[i].val).isnumeric() != True: 
                            if(n[i].exp == ExpressionType.Op):
                                if st_lookup_general(n[i].child[0].val, linkedList, 1) != 'int':
                                    if st_lookup_toLast(n[i].child[0].val, linkedList) != 'int':
                                        if st_lookup_general(n[i].child[1].val, linkedList, 1) != 'int':
                                            if st_lookup_toLast(n[i].child[1].val, linkedList) != 'int':
                                                typeError(t,"The arguments must be 'int'", n[i].val)
                            else:
                                if st_lookup_general(n[i].val, linkedList, 1) != 'int':
                                    if st_lookup_toLast(n[i].val, linkedList) != 'int':
                                        typeError(t,"Parameters error", n[i].val)
                
# tableNumber se utiliza para poder darle el número de scope a las tablas y para identificar
# si es la primera tabla (global)
global tableNumber 
tableNumber = 0 

# Mediante condicionales, se identifica el tipo de expresión de cada nodo para que 
# se pueda ir insertando en la tabla mediante la función st_insert().
def insertNode(t):
    global location, tableNumber, BucketList

    if t.exp == ExpressionType.Params:
        if tableNumber == 0:
            linkedList.push("GlOBAL TABLE", BucketList, str(tableNumber))
            BucketList = {}
            tableNumber+=1
        else:
            linkedList.push("SCOPE "+str(tableNumber), BucketList, str(tableNumber))
            BucketList = {}
            tableNumber+=1

    if t.exp == ExpressionType.ListDeclaration:
        temp = []
        for i in range(-1, (len(t.child)-24)*-1, -1):
            if (st_lookup(BucketList, t.child[i].val) == -1):
                if t.child[i].child[1]:
                    functionVar = t.child[i].child[1]
                    if functionVar.exp == ExpressionType.Function:
                        if t.child[i].child[1].child[0].child[-1]:
                            paramList = t.child[i].child[1].child[0].child[-1]
                            if paramList.exp == ExpressionType.ParamList:
                                for j in range(len(paramList.child)):
                                    if paramList.child[j] != None:
                                        if paramList.child[j].child[1]:
                                            temp.append("Array") 
                                        else:
                                            temp.append("Const")  
                                st_insert(BucketList, t.child[i].child[0].val,t.child[i].val,"Function", temp)
                                temp = []
                            else:
                                st_insert(BucketList, t.child[i].child[0].val,t.child[i].val,"Function", "void")      
                    else:
                        st_insert(BucketList, t.child[i].child[0].val,t.child[i].val,"Array", t.child[i].child[1].val, t.lineno)
                else:
                    dec = list(filter(None, t.child[i].child))
                    st_insert(BucketList, dec[0].val, t.child[i].val,"Const",None, t.lineno)
                
    if t.exp == ExpressionType.ParamList:
        for i in range(-1, (len(t.child)-24)*-1, -1):
            if (st_lookup(BucketList, t.child[i].val) == -1):
                if t.child[i].child[1]:
                    st_insert(BucketList, t.child[i].child[0].val,t.child[i].val,"Array", None, t.lineno)
                else:
                    st_insert(BucketList, t.child[i].child[0].val,t.child[i].val,"Const",None, t.lineno)
    
# Se inserta el ultimo scope y se imprime cada tabla con su nombre.
def tabla(syntaxTree, imprime):
        global linkedList, tableNumber, BucketList
        traverse(syntaxTree, insertNode, nullProc)
        # Esta línea es para insertar el último scope a la tabla.
        linkedList.push("SCOPE "+str(tableNumber), BucketList, str(tableNumber))
        tableNumber+=1
        if (imprime):
            linkedList = linkedList.head
            temp = linkedList
            while temp:
                print()
                print()
                print()
                print(temp.name)
                print()
                printSymTab(temp.data)
                temp = temp.next             
            
def semantica(tree, imprime=True):
    tabla(tree, imprime)
    typeCheck(tree)

def typeCheck(syntaxTree):
    traverse(syntaxTree,nullProc,checkNode)
