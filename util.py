import os

SEP = "."

def search(x, y, list):
    i = 0
    for el in list:
        if (el[0] == x and el[1] == y):
            return i
        i += 1
    return None
#
def add(list, x, y):
    if (search(x, y, list) == None):
        list.append((x, y))
        list.sort()
    else:
        raise ValueError("("+str(x)+" "+str(y)+") est deja explore")
#
def remove(list, x, y):
    index = search(x, y, list)
    if (index == None):
        raise ValueError("("+str(x)+" "+str(y)+") n'est pas encore explore")
    list.pop(index)
#
def save(filename, list, lastentered):
    file = open(filename, "w+")
    #file.write(lastentered+"\n")
    for el in list:
        file.write(str(el[0])+SEP+str(el[1])+"\n")
    file.close()
#
def load(filename):
    mode = "r+"
    if (not os.path.exists(filename)):
        mode = "w+"
    file = open(filename, mode)
    list = []
    for line in file:
        Line = line.strip().split(SEP)
        list.append((int(Line[0]),int(Line[1])))
    list.sort()
    file.close()
    return list
#
