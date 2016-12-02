import os, sys
import traceback

import core, map

datadir = core.datadir

mapwords = core.loadWords(datadir+"words_map.txt")
savewords = core.loadWords(datadir+"words_save.txt")
viewwords = core.loadWords(datadir+"words_view.txt")
exitwords = core.loadWords(datadir+"words_exit.txt")
exitwords_reserved = ("quit", "exit")
planet_names = core.loadWords(datadir+"planet_names.txt")
planets = {}
for planetname in planet_names:
    planets[planetname] = []
planets_loaded = False
reservedwords = ["zone", "d", "help"] + planet_names

core.removefromlist(mapwords, reservedwords)
core.removefromlist(savewords, reservedwords)
core.removefromlist(exitwords, reservedwords)

if (len(mapwords) == 0):
    mapwords.append("map")
if (len(savewords) == 0):
    savewords.append("save")
for exit_word in exitwords_reserved:
    if (not exit_word in exitwords):
        exitwords.append(exit_word)
#
playername = ""
if (len(sys.argv) >= 2):
    playername = sys.argv[1].strip().lower()
    if (core.isforbidden(playername) or playername in exitwords_reserved):
        playername = raw_input("Entrez votre pseudo: ")
else:
    playername = raw_input("Entrez votre pseudo: ")
#
playername = playername.strip().lower()
if (core.isforbidden(playername)):
    print "Erreur: ce pseudo est interdit"
    sys.exit(0)
elif (playername in exitwords_reserved):
    sys.exit(0)
list = core.load(playername)
Str = ""
Strlist = []
print 'Tapez "help" pour obtenir de l\'aide'
b = False
try:
    while (not core.oneIn(exitwords, Strlist)):
        Str = raw_input("> ").strip().lower()
        Strlist = Str.split(" ")
        try:
            if ("help" in Strlist):
                if (len(Strlist) == 1):
                    print 'Tapez "x y" pour marquer le secteur aux coordonnees (x, y) exploree.'
                    print 'Tapez "zone x1 y1 x2 y2" pour marquer comme explore chaque secteur situe dans le rectangle decrit par les coordonnees (x1, y1) et (x2, y2).'
                    print 'Entrez le nom d\'une planete pour marquer chacun de ses secteurs comme explore. Exception pour la Terre.'
                    print 'Liste des planetes: '+str(planet_names)
                    print 'Dans les commandes precedentes, l\'option "d" a pour effet de marquer comme non explore.'
                    print "Pour quitter ce script, entrez l'un des mots suivants: "+str(exitwords)
                    print 'Pour les autres commandes, tapez "help commandname" pour obtenir des informations supplementaires.'
                    print 'Valeurs possibles de "commandname" pour generer la carte: '+str(mapwords)
                    print 'Valeurs possibles de "commandname" pour sauvegarder les donnees: '+str(savewords)
                else:
                    if (core.oneIn(mapwords, Strlist)):
                        print "Coming soon"
                    elif (core.oneIn(savewords, Strlist)):
                        print "Coming soon"
                    elif (core.oneIn(planet_names, Strlist)):
                        print "Coming soon"
                    else:
                        Strlist.remove("help")
                        tempstring = " ".join(Strlist)
                        print 'Aucune commande du nom de "'+tempstring+'"'
            elif (core.oneIn(mapwords, Strlist)):
                if (not planets_loaded):
                    core.loadPlanets(datadir+"coords_planets.txt", planets)
                    planets_loaded = True
                map.makeMap(playername, list, planets)
            elif (core.oneIn(savewords, Strlist)):
                core.save(playername, list, None)
            elif (core.oneIn(viewwords, Strlist)):
                os.system(map.getMapFilename(playername))
            elif (core.oneIn(exitwords, Strlist)):
                pass #nothing to do
            elif ("zone" in Strlist):
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
            elif (core.oneIn(planet_names, Strlist)):
                if (not planets_loaded):
                    core.loadPlanets(datadir+"coords_planets.txt", planets)
                    planets_loaded = True
                name = ""
                for planetname in planet_names:
                    if (planetname in Strlist):
                        name = planetname
                        break
                if (name == ""):
                    raise ValueError("unknown error")
                if ("d" in Strlist):
                    for (x, y) in planets[name]:
                        try:
                            core.remove(list, x, y)
                        except ValueError, e:
                            print e
                        except Exception, e:
                            traceback.print_exc()
                else:
                    for (x, y) in planets[name]:
                        try:
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
        except Exception, e:
            if (Str != ""):
                traceback.print_exc()
except KeyboardInterrupt, e:
    pass
except Exception, e:
    traceback.print_exc()
#
