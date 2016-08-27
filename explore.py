import os
import util

#Str = raw_input("Entrez votre pseudo: ")+".txt"
Str = "spirou003"+".txt"
try:
    filename = Str
    list = util.load(filename)
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
                (x, y) = Str.strip().split(" ")
                x = int(x)
                y = int(y)
                try:
                    if (b):
                        util.remove(list, x, y)
                    else:
                        util.add(list, x, y)
                except ValueError, e:
                    print e
                except Exception, e:
                    print "une erreur est survenue: "+str(e)
            except Exception, e:
                if ("save" in Str.lower()):
                    util.save(filename, list, None)
    except KeyboardInterrupt, e:
        util.save(filename, list, None)
    except Exception, e:
        print e
except Exception, e:
    print e