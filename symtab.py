# the hash table
BucketList = {}

# Procedure st_insert inserts line numbers and
# memory locations into the symbol table
# loc = memory location is inserted only the
# first time, otherwise ignored
def st_insert(BucketList, key, type, structure, value, lineno=""):
    if key in BucketList:
        BucketList[key].append(value)
    else:
        BucketList[key] = [type, structure, value, lineno]

# Function st_lookup returns the memory 
# location of a variable or -1 if not found
def st_lookup(BucketList, key):
    if key in BucketList:
        return BucketList[key][0]
    else:
        return -1

# Se utiliza para bucar los valores de la tabla, y dependiendo se es una funcion (0), arumentos(1) o un parámetro 2.
def st_lookup_general(key, list, num):
    if key in list.data:
        return list.data[key][num]
    else:
        if list.next == None:
            return -1
        list = list.next
        return st_lookup_general(key, list, num) 

# Se utiliza para comparar el valor del último nodo (que es la global table) respecto a la variable con la que estamos. 
def st_lookup_toLast(key, list):
    # while list.next != None:
    #     list = list.next
    if key in list.data:
        return list.data[key][0]
    else:
        return -1
        

def st_information_lp(key, table):
    if key in table.data:
        return table.data[key][2]
    else:
        if table.next == None:
            return -1
        table = table.next
        return st_information_lp(key, table) 


def st_scope_lp(key, table):
    if key in table.data:
        return table.scope
    else:
        if table.next == None:
            return -1
        table = table.next
        return st_scope_lp(key, table) 


def st_information_ins(key, table, value):
    if key in table.data:
        table.data[key][2] = value
    else:
        if table.next == None:
            return -1
        table = table.next
        return st_information_ins(key, table, value) 

# Procedure printSymTab prints a formatted 
# listing of the symbol table contents 
# to the listing file
def printSymTab(BucketList):
    print("Key            Type           Structure       Value ")
    print("---            ----           ---------       ------")
    for key in BucketList:
        print(f'{key:15}{BucketList[key][0]}\t      ', end = '')
        for i in range(len(BucketList[key])-3):
            print(f'{BucketList[key][i+1]}\t      ', end = '')
        print(f'{BucketList[key][2]}\t      ', end = '')
        print()
