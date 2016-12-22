#coding: utf-8
import os, sys
import traceback
import itertools

import Core, Map, Data
xrange = Core.getxrange()
raw_input = Core.getraw_input()

CONFIGDIR = Core.CONFIGDIR
SAVEDIR = Core.SAVEDIR

def Main():
    if (not os.path.isdir(CONFIGDIR)):
        print("Impossible de demarrer: le dossier "+CONFIGDIR+" est manquant.")
        system.exit(0)
    if (not os.path.isdir(SAVEDIR)):
        os.mkdir(SAVEDIR)

    planets = Data.loadPlanets(CONFIGDIR+"coords_planets.txt")
    planet_names = list(planets.keys())
    reservedwords = ["zone", "d", "help"] + planet_names

    commands = Core.readconfigfile(CONFIGDIR+"words.txt")
    
    #make sure that dictionnary contains all used keys
    for key in ["map", "save", "target", "view", "exit", "set-terre"]:
        if (key not in commands or "words" not in commands[key]):
            commands[key] = {"words":key}
    #
    #get set of words for each command (instead of space-separated string)
    #keep only non reserved words, but at least one
    for key in commands:
        if "words" in commands[key]:
            commands[key]["words"] = set(commands[key]["words"].split())
            Core.removefromlist(commands[key]["words"], reservedwords)
            if (len(commands[key]["words"]) == 0):
                commands[key]["words"].add(key)
    #
    #use some standard words to exit prompt
    exitwords_reserved = ("quit", "exit")
    for exit_word in exitwords_reserved:
        if (not exit_word in commands["exit"]["words"]):
            commands["exit"]["words"].add(exit_word)
    #
    playername = ""
    if (len(sys.argv) >= 2):
        playername = sys.argv[1].strip().lower()
    if (Core.isforbidden(playername) or playername in exitwords_reserved):
        playername = raw_input("Entrez votre pseudo: ")
    playername = playername.strip().lower()
    if (Core.isforbidden(playername)):
        print("Erreur: ce pseudo est interdit")
        sys.exit(0)
    elif (playername in exitwords_reserved):
        sys.exit(0)
    playerdata = Data.load(playername)
    settings = playerdata[2]
    if (playername not in settings):
        settings[playername] = {}
    settings = settings[playername]
    if ("terre" in settings):
        planet_names = addTerre(settings, settings["terre"].split(), planets)
    Str = ""
    Strlist = []
    print('Tapez "help" pour obtenir de l\'aide')
    try:
        while (not Core.oneIn(commands["exit"]["words"], Strlist)):
            Str = raw_input("> ").strip().lower()
            if (Str == ""):
                continue
            Strlist = Str.split(" ")
            try:
                if ("help" in Strlist):
                    if (len(Strlist) == 1):
                        print('Tapez "x y" pour marquer le secteur aux coordonnees (x, y) exploree.')
                        print('Tapez "zone x1 y1 x2 y2" pour marquer comme explore chaque secteur situe dans le rectangle decrit par les coordonnees (x1, y1) et (x2, y2).')
                        print("Entrez le nom d'une planete pour marquer chacun de ses secteurs comme explore. Exception pour la Terre.")
                        print('Liste des planetes: '+str(planet_names))
                        print('Dans les commandes precedentes, l\'option "d" a pour effet de marquer comme non explore.')
                        print("Pour quitter ce script, entrez l'un des mots suivants: "+str(commands["exit"]["words"]))
                        print('Pour les autres commandes, tapez "help commandname" pour obtenir des informations supplementaires.')
                        print('Valeurs possibles de "commandname" pour generer la carte: '+str(commands["map"]["words"]))
                        print('Valeurs possibles de "commandname" pour sauvegarder les donnees: '+str(commands["save"]["words"]))
                    else:
                        if (Core.oneIn(commands["map"]["words"], Strlist)):
                            print("Coming soon")
                        elif (Core.oneIn(commands["save"]["words"], Strlist)):
                            print("Coming soon")
                        elif (Core.oneIn(planet_names, Strlist)):
                            print("Coming soon")
                        else:
                            Strlist.remove("help")
                            tempstring = " ".join(Strlist)
                            print('Aucune commande du nom de "'+tempstring+'"')
                elif (Core.oneIn(commands["map"]["words"], Strlist)):
                    Map.makeMap(playername, playerdata, planets)
                elif (Core.oneIn(commands["save"]["words"], Strlist)):
                    Data.save(playername, playerdata)
                elif (Core.oneIn(commands["view"]["words"], Strlist)):
                    os.system(Map.getMapFilename(playername))
                elif (Core.oneIn(commands["target"]["words"], Strlist)):
                    print('Entrez vos nouveaux objectifs:')
                    while (not Core.oneIn(commands["exit"]["words"], Strlist)):
                        Str = raw_input("==> ").strip().lower()
                        if (Str == ""):
                            continue
                        Strlist = Str.split(" ")
                        if (Core.oneIn(commands["exit"]["words"], Strlist)):
                            pass #nothing to do
                        else:
                            (coords, explore) = parsecoords(Str, Strlist, planet_names, planets)
                            if (explore):
                                Data.addtarget(playerdata, coords)
                            else:
                                Data.deltarget(playerdata, coords)
                    Strlist = [] #don't exit immediately after that
                elif (Core.oneIn(commands["set-terre"]["words"], Strlist)):
                    print('Entrez les coordonnees de votre terre:')
                    while (not Core.oneIn(commands["exit"]["words"], Strlist)):
                        Str = raw_input("==> ").strip().lower()
                        if (Str == ""):
                            continue
                        Strlist = Str.split(" ")
                        if (Core.oneIn(commands["exit"]["words"], Strlist)):
                            pass #nothing to do
                        else:
                            (coords, explore) = parsecoords(Str, Strlist, planet_names, planets)
                            if (len(coords) != 1):
                                print("Indiquez les coordonnees ecrites sur la carte PID")
                            else:
                                planet_names = addTerre(settings, coords[0], planets)
                                break
                    Strlist = [] #don't exit immediately after that
                elif (Core.oneIn(commands["exit"]["words"], Strlist)):
                    pass #nothing to do
                else:
                    (coords, explore) = parsecoords(Str, Strlist, planet_names, planets)
                    if (explore):
                        Data.explore(playerdata, coords)
                    else:
                        Data.unexplore(playerdata, coords)
            except Exception as e:
                traceback.print_exc()
    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        traceback.print_exc()
#
def parsecoords(Str, Strlist, planet_names, planets):
    def _parsecoords(Str, Strlist, planet_names, planets):
        if ("zone" in Strlist):
            Strlist.remove("zone")
            if (len(Strlist) != 4):
                print('Commande incorrecte: "'+Str+'"')
                missing = 4-len(Strlist);
                if (missing < 0):
                    print("Il y a "+str(-missing)+" argument(s) en trop.")
                else:
                    print("Il manque "+str(missing)+" argument(s).")
                return []
            (x1, y1, x2, y2) = Strlist
            if (not (Core.isint(x1) and Core.isint(x2) and Core.isint(y1) and Core.isint(y2))):
                print('Commande incorrecte: "'+Str+'"')
                if (not Core.isint(x1)):
                    print("L'argument n°1 n'est pas un nombre entier.")
                if (not Core.isint(y1)):
                    print("L'argument n°2 n'est pas un nombre entier.")
                if (not Core.isint(x2)):
                    print("L'argument n°3 n'est pas un nombre entier.")
                if (not Core.isint(y2)):
                    print("L'argument n°4 n'est pas un nombre entier.")
                return []
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            (x1, x2) = (min(x1, x2), max(x1, x2))
            (y1, y2) = (min(y1, y2), max(y1, y2))
            return itertools.product(xrange(x1, x2+1), xrange(y1, y2+1))
        elif (Core.oneIn(planet_names, Strlist)):
            name = ""
            for planetname in planet_names:
                if (planetname in Strlist):
                    name = planetname
                    break
            return planets[name]
        else:
            if (len(Strlist) != 2):
                print('Commande incorrecte: "'+Str+'"')
                missing = 2-len(Strlist)
                if (missing < 0):
                    print("Il y a "+str(-missing)+" argument(s) en trop.")
                else:
                    print("Il manque "+str(missing)+" argument(s).")
                return []
            (x, y) = Strlist
            if (not (Core.isint(x) and Core.isint(y))):
                print('Commande incorrecte: "'+Str+'"')
                if (not Core.isint(x)):
                    print("L'argument n°1 n'est pas un nombre entier.")
                if (not Core.isint(y)):
                    print("L'argument n°2 n'est pas un nombre entier.")
                return []
            x = int(x)
            y = int(y)
            return [(x, y)]
    explore = ('d' not in Strlist)
    if (not explore):
        Strlist.remove("d")
    return (_parsecoords(Str, Strlist, planet_names, planets), explore)
#
def addTerre(settings, coords, planets):
    settings["terre"] = [str(coords[0]), str(coords[1])]
    planets["terre"] = Data.getTerreCoords(int(coords[0]), int(coords[1]))
    return list(planets.keys())
#
Main()
