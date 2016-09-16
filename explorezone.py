import os
import core

Str = raw_input("Entrez votre pseudo: ")+".txt"
try:
    filename = Str
    list = core.load(filename)
    Str = ""
    print 'Pour desexplorer, tapez "d" devant les coordonnees "x1 y1 x2 y2"'
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
                                core.remove(list, x, y)
                            else:
                                core.add(list, x, y)
                        except ValueError, e:
                            print e
                        except Exception, e:
                            print "une erreur est survenue: "+str(e)
            except Exception, e:
                if ("save" in Str.lower()):
                    core.save(filename, list, None)
    except KeyboardInterrupt, e:
        core.save(filename, list, None)
    except Exception, e:
        print e
except Exception, e:
    print e