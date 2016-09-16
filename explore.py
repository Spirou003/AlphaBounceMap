import os, sys
import traceback
import core

mapwords = core.loadWords("words_map.txt")
savewords = core.loadWords("words_save.txt")

#playername = raw_input("Entrez votre pseudo: ")
playername = "spirou003"
Str = playername+".txt"
try:
    filename = Str
    list = core.load(filename)
    Str = ""
    print 'Pour desexplorer, tapez "d" devant les coordonnees "x y"'
    try:
        b = False
        while (True):
            Str = raw_input("> ")
            if (core.oneIn(mapwords, Str)):
                core.makeMap(playername, list)
            elif (core.oneIn(savewords, Str)):
                core.save(filename, list, None)
            else:
                try:
                    b = (Str[0] == 'd')
                    if (b):
                        Str = Str[1:]
                    (x, y) = Str.strip().split(" ")
                    x = int(x)
                    y = int(y)
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