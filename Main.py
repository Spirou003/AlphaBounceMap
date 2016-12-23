#coding: utf-8
import os, sys
import traceback
import itertools

import Core, Map, Data
from Compatibility import *

CONFIGDIR = Core.CONFIGDIR
SAVEDIR = Core.SAVEDIR

def Main():
    if (not os.path.isdir(CONFIGDIR)):
        printf("Impossible de démarrer: le dossier "+CONFIGDIR+" est manquant.")
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
        printf("Erreur: ce pseudo est interdit")
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
    printf('Tapez "help" pour obtenir de l\'aide')
    try:
        while (not Core.oneIn(commands["exit"]["words"], Strlist)):
            Str = raw_input("> ").strip().lower()
            if (Str == ""):
                continue
            Strlist = Str.split(" ")
            try:
                if ("help" in Strlist):
                    print_help(Strlist, commands, planet_names)
                elif (Core.oneIn(commands["map"]["words"], Strlist)):
                    Map.makeMap(playername, playerdata, planets)
                elif (Core.oneIn(commands["save"]["words"], Strlist)):
                    Data.save(playername, playerdata)
                elif (Core.oneIn(commands["view"]["words"], Strlist)):
                    os.system(Map.getMapFilename(playername))
                elif (Core.oneIn(commands["target"]["words"], Strlist)):
                    printf('Entrez vos nouveaux objectifs:')
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
                    printf('Entrez les coordonnées de votre terre:')
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
                                printf("Indiquez les coordonnées écrites sur la carte PID")
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
                printf('Commande incorrecte: "'+Str+'"')
                missing = 4-len(Strlist);
                if (missing < 0):
                    printf("Il y a "+str(-missing)+" argument(s) en trop.")
                else:
                    printf("Il manque "+str(missing)+" argument(s).")
                return []
            (x1, y1, x2, y2) = Strlist
            if (not (Core.isint(x1) and Core.isint(x2) and Core.isint(y1) and Core.isint(y2))):
                printf('Commande incorrecte: "'+Str+'"')
                if (not Core.isint(x1)):
                    printf("L'argument n°1 n'est pas un nombre entier.")
                if (not Core.isint(y1)):
                    printf("L'argument n°2 n'est pas un nombre entier.")
                if (not Core.isint(x2)):
                    printf("L'argument n°3 n'est pas un nombre entier.")
                if (not Core.isint(y2)):
                    printf("L'argument n°4 n'est pas un nombre entier.")
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
                printf('Commande incorrecte: "'+Str+'"')
                missing = 2-len(Strlist)
                if (missing < 0):
                    printf("Il y a "+str(-missing)+" argument(s) en trop.")
                else:
                    printf("Il manque "+str(missing)+" argument(s).")
                return []
            (x, y) = Strlist
            if (not (Core.isint(x) and Core.isint(y))):
                printf('Commande incorrecte: "'+Str+'"')
                if (not Core.isint(x)):
                    printf("L'argument n°1 n'est pas un nombre entier.")
                if (not Core.isint(y)):
                    printf("L'argument n°2 n'est pas un nombre entier.")
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
def printwords(words):
    return '"'+'", "'.join(words).strip('"').strip()+'"'
#
def print_help(Strlist, commands, planet_names):
    if (len(Strlist) == 1):
        printf('Tapez "x y" pour marquer le secteur aux coordonnées (x, y) exploré.')
        printf('Tapez "zone x1 y1 x2 y2" pour marquer comme exploré chaque secteur situé dans le rectangle décrit par les coordonnées (x1, y1) et (x2, y2).')
        printf("Entrez le nom d'une planète pour marquer chacun de ses secteurs comme exploré.")
        printf('Liste des planètes: '+printwords(planet_names))
        printf('Dans les commandes précédentes, l\'option "d" a pour effet de marquer comme non exploré un secteur exploré.')
        printf("Pour quitter ce script, entrez l'un des mots suivants: "+printwords(commands["exit"]["words"]))
        printf('Pour les autres commandes, tapez "help commandname" pour obtenir des informations supplémentaires.')
        printf('Valeurs possibles de "commandname" pour générer la carte: '+printwords(commands["map"]["words"]))
        printf('Valeurs possibles de "commandname" pour sauvegarder les données: '+printwords(commands["save"]["words"]))
        printf('Valeurs possibles de "commandname" pour modifier les objectifs: '+printwords(commands["target"]["words"]))
        printf('Valeurs possibles de "commandname" pour situer la Terre: '+printwords(commands["set-terre"]["words"]))
    else:
        if (Core.oneIn(commands["map"]["words"], Strlist)):
            printf("La taille de la map est calculée sur base des critères suivants:")
            printf("- Elle doit afficher tous les éléments de l'univers (planètes, astéroïdes)")
            printf("- Elle doit afficher tous les autres éléments spécifiés dans le dossier config")
            printf("- Elle doit reprendre toutes les explorations d'un joueur ainsi que tous ses objectifs")
            printf("Les pixels de l'image représentent les secteurs qui sont dessinés sur la map")
            printf("- Chaque pixel est marqué comme non exploré")
            printf("- Chaque secteur exploré est reporté, indépendament de son type (planète, astéroïde, ...)")
            printf("- Les éléments spéciaux sont ensuite dessinés (en tenant compte des objectifs et explorations)")
            printf("- Les secteurs désignés comme objectif qui ne le sont pas encore sont alors dessinés")
            printf("- Pour finir, des axes sont tracés par dessus la map obtenue")
            printf("La map est enregistrée dans le dossier saves au nom de \""+str(playername)+".png\"")
            printf("À chaque étape de la création de la map, la couleur obtenue est calculée sur base de:")
            printf("- La couleur actuelle du pixel")
            printf("- La couleur de l'élément à dessiner (varie selon le type de secteur et s'il est exploré ou objectif)")
            printf("- La couleur de l'élément à dessiner est prioritaire sur la couleur du secteur:")
            printf("--> Plus la nouvelle couleur est opaque, moins l'ancienne couleur sera visible")
            printf("")
            printf("Les couleurs peuvent être paramétrées via le fichier \"config"+os.sep+"colors.ini")
        elif (Core.oneIn(commands["save"]["words"], Strlist)):
            printf("Enregistre les données du joueur dans plusieurs fichiers du dossier saves:")
            printf("- "+str(playername)+".txt: regroupe tous les secteurs explorés")
            printf("--> Un secteur = une ligne, dont la structure est x"+Data.SEP+"y")
            printf(" "+str(playername)+".objectifs.txt: regroupe tous les secteurs considérés comme objectif")
            printf("--> Un secteur = une ligne, dont la structure est x"+Data.SEP+"y")
            printf(" "+str(playername)+".infos.txt: regroupe diverses informations sous forme d'un fichier ini")
            printf("--> La position de la terre (si elle est connue), notée x y")
        elif (Core.oneIn(commands["target"]["words"], Strlist)):
            printf("Coming soon")
        elif (Core.oneIn(commands["set-terre"]["words"], Strlist)):
            printf("Coming soon")
        elif (Core.oneIn(planet_names, Strlist)):
            printf("Coming soon")
        else:
            Strlist.remove("help")
            tempstring = " ".join(Strlist)
            printf('Aucune commande du nom de "'+tempstring+'"')
#
Main()
