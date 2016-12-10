import os, sys
import traceback

import Core, Map, Data

DATADIR = Core.DATADIR
SAVEDIR = Data.SAVEDIR

if (not os.path.isdir("saves")):
    os.mkdir("saves")

planets = Data.loadPlanets(DATADIR+"coords_planets.txt")
planet_names = planets.keys()
reservedwords = ["zone", "d", "help"] + planet_names

mapwords = Core.loadWords(DATADIR+"words_map.txt")
Core.removefromlist(mapwords, reservedwords)
if (len(mapwords) == 0):
    mapwords.append("map")

savewords = Core.loadWords(DATADIR+"words_save.txt")
Core.removefromlist(savewords, reservedwords)
if (len(savewords) == 0):
    savewords.append("save")

viewwords = Core.loadWords(DATADIR+"words_view.txt")
Core.removefromlist(viewwords, reservedwords)
if (len(viewwords) == 0):
    viewwords.append("view")

exitwords = Core.loadWords(DATADIR+"words_exit.txt")
Core.removefromlist(exitwords, reservedwords)
exitwords_reserved = ("quit", "exit")
for exit_word in exitwords_reserved:
    if (not exit_word in exitwords):
        exitwords.append(exit_word)
#
playername = ""
if (len(sys.argv) >= 2):
    playername = sys.argv[1].strip().lower()
if (Core.isforbidden(playername) or playername in exitwords_reserved):
    playername = raw_input("Entrez votre pseudo: ")
playername = playername.strip().lower()
if (Core.isforbidden(playername)):
    print "Erreur: ce pseudo est interdit"
    sys.exit(0)
elif (playername in exitwords_reserved):
    sys.exit(0)
explorations = Data.load(playername)
Str = ""
Strlist = []
print 'Tapez "help" pour obtenir de l\'aide'
try:
    while (not Core.oneIn(exitwords, Strlist)):
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
                    if (Core.oneIn(mapwords, Strlist)):
                        print "Coming soon"
                    elif (Core.oneIn(savewords, Strlist)):
                        print "Coming soon"
                    elif (Core.oneIn(planet_names, Strlist)):
                        print "Coming soon"
                    else:
                        Strlist.remove("help")
                        tempstring = " ".join(Strlist)
                        print 'Aucune commande du nom de "'+tempstring+'"'
            elif (Core.oneIn(mapwords, Strlist)):
                Map.makeMap(playername, explorations, planets)
            elif (Core.oneIn(savewords, Strlist)):
                Data.save(playername, explorations, None)
            elif (Core.oneIn(viewwords, Strlist)):
                os.system(Map.getMapFilename(playername))
            elif (Core.oneIn(exitwords, Strlist)):
                pass #nothing to do
            elif ("zone" in Strlist):
                Strlist.remove("zone")
                unexplore = ('d' in Strlist)
                if (unexplore):
                    Strlist.remove("d")
                (x1, y1, x2, y2) = Strlist
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                if (unexplore):
                    Data.unexplorezone(explorations, x1, y1, x2, y2)
                else:
                    Data.explorezone(explorations, x1, y1, x2, y2)
            elif (Core.oneIn(planet_names, Strlist)):
                unexplore = ("d" in Strlist)
                if (unexplore):
                    Strlist.remove("d")
                name = ""
                for planetname in planet_names:
                    if (planetname in Strlist):
                        name = planetname
                        break
                if (unexplore):
                    Data.unexploreplanet(explorations, planets, name)
                else:
                    Data.exploreplanet(explorations, planets, name)
            else:
                unexplore = ('d' in Strlist)
                if (unexplore):
                    Strlist.remove("d")
                (x, y) = Strlist
                x = int(x)
                y = int(y)
                try:
                    if (unexplore):
                        Data.unexplore(explorations, x, y)
                    else:
                        Data.explore(explorations, x, y)
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
