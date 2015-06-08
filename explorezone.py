import os

SEP = "."

def search(x, y, list):
    i = 0
    for el in list:
        if (el[0] == x and el[1] == y):
            return i
        i += 1
    return None

mode = "r+"
Str = raw_input("Entrez votre pseudo: ")+".txt"
if (not os.path.exists(Str)):
    mode = "w+"
try:
    file = open(Str, mode)
    list = []
    for line in file:
        Line = line.strip().split(SEP)
        list.append((int(Line[0]),int(Line[1])))
    list.sort()
    file.close()
    filename = Str
    Str = ""
    print 'Pour desexplorer, tapez "d" devant les coordonnees "x y"'
    try:
        b = False
        while (True):
            Str = raw_input("Coordonnees explorees: ")
            try:
                b = (Str[0] == 'd')
                if (b):
                    Str = Str[1:]
                (x1, y1, x2, y2) = Str.strip().split(" ")
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                (x1, x2) = (min(x1, x2), max(x1, x2))
                (y1, y2) = (min(y1, y2), max(y1, y2))
                for x in xrange(x1, x2+1):
                    for y in xrange(y1, y2+1):
                        try:
                            if (b):
                                list.pop(search(x, y, list))
                                list.sort()
                            else:
                                if (search(x, y, list) == None):
                                    list.append((x, y))
                                else:
                                    raise Exception()
                        except Exception, e:
                            if (b):
                                print "("+str(x)+" "+str(y)+") n'est pas encore explore"
                            else:
                                print "("+str(x)+" "+str(y)+") est deja explore"
                list.sort()
            except Exception, e:
                pass
    except KeyboardInterrupt, e:
        file = open(filename, "w+")
        for el in list:
            file.write(str(el[0])+SEP+str(el[1])+"\n")
        file.close()
    except Exception, e:
        print e
except Exception, e:
    print e