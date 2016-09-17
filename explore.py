import os, sys
import traceback
import core

mapwords = core.loadWords("words_map.txt")
savewords = core.loadWords("words_save.txt")
exitwords = core.loadWords("words_exit.txt")

playername = ""
if (len(sys.argv) < 2):
    playername = raw_input("Entrez votre pseudo: ")
else:
    playername = sys.argv[1]
Str = playername+".txt"

filename = Str
list = core.load(filename)
Str = ""
print 'Tapez "help" pour obtenir de l\'aide'
b = False
try:
    while (not core.oneIn(exitwords, Str)):
        Str = raw_input("> ")
        Strlist = Str.strip().lower().split(" ")
        try:
            if (core.oneIn(Strlist, "help")):
                if (len(Strlist) == 1):
                    print 'Tapez "x y" pour marquer le secteur aux coordonnees (x, y) exploree.'
                    print 'Tapez "zone x1 y1 x2 y2" pour marquer comme explore chaque secteur situe dans le rectangle decrit par les coordonnees (x1, y1) et (x2, y2).'
                    print 'Dans les commandes precedentes, l\'option "d" a pour effet de marquer comme non explore.'
                    print "Pour quitter ce script, entrez l'un des mots suivants: "+str(exitwords)
                    print 'Pour les autres commandes, tapez "help commandname" pour obtenir des informations supplementaires.'
                    print 'Valeurs possibles de "commandname" pour generer la carte: '+str(mapwords)
                    print 'Valeurs possibles de "commandname" pour sauvegarder les donnees: '+str(savewords)
                else:
                    pass
            elif (core.oneIn(mapwords, Str)):
                core.makeMap(playername, list)
            elif (core.oneIn(savewords, Str)):
                core.save(filename, list, None)
            elif (core.oneIn(exitwords, Str)):
                pass #nothing to do
            else:
                if (core.oneIn(Strlist, "zone")):
                    Strlist.remove("zone")
                    b = ('d' in Strlist)
                    if (b):
                        Strlist.remove("d")
                    (x1, y1, x2, y2) = Strlist
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
                                traceback.print_exc()
                else:
                    b = ('d' in Strlist)
                    if (b):
                        Strlist.remove("d")
                    (x, y) = Strlist
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
            traceback.print_exc()
except KeyboardInterrupt, e:
    pass
except Exception, e:
    traceback.print_exc()
#
