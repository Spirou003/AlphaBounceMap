#coding: utf-8
import os
import traceback

import Core
xrange = Core.getxrange()
raw_input = Core.getraw_input()


SEP = "."

def printablecoords(x, y):
    return "("+str(x)+" : "+str(y)+")"
#
def readcoordsfile(filename, mode = "r"):
    if (not os.path.exists(filename)):
        return set()
    file = open(filename, mode)
    coords = set()
    for line in file:
        Line = line.strip()
        try:
            if ('[' == Line[0]):
                tmp = Line[1:-1].split("] ... [")
                (x1,y1) = tmp[0].split(",")
                (x2,y2) = tmp[1].split("][")
                (x1,x2,y1,y2) = (int(x1),int(x2),int(y1),int(y2))
                for x in xrange(x1, x2+1):
                    for y in xrange(y1, y2+1):
                        coords.add((x, y))
            else:
                tmp = Line.split(SEP)
                coords.add((int(tmp[0]),int(tmp[1])))
        except Exception as e:
            print(str(filename)+": format invalide: "+Line)
    file.close()
    return coords
#
def mark(playerdata, coords, remarkmsg, targetmsg):
    for (x, y) in coords:
        if ((x, y) not in playerdata[0]):
            playerdata[0].add((x, y))
        else:
            print(remarkmsg(printablecoords(x, y)))
        if ((x, y) in playerdata[1]):
            playerdata[1].remove((x, y))
            print(targetmsg(printablecoords(x, y)))
#
def unmark(playerdata, coords, reunmarkmsg):
    for (x, y) in coords:
        if ((x, y) not in playerdata[0]):
            print(reunmarkmsg(printablecoords(x, y)))
        else:
            playerdata[0].remove((x, y))
#
def explore(playerdata, coords):
    mark(playerdata, coords, lambda w:str(w)+" est deja explore",lambda w:"Objectif atteint: "+str(w))
#
def unexplore(playerdata, coords):
    unmark(playerdata, coords, lambda w:str(w)+" n'est pas encore explore")
#
def addtarget(playerdata, coords):
    mark((playerdata[1],[]), coords, lambda w:str(w)+" est deja un objectif",lambda w:"Erreur: cela ne doit jamais arriver!!!")
#
def deltarget(playerdata, coords):
    unmark((playerdata[1],[]), coords, lambda w:str(w)+" n'etait pas un objectif")
#
def save(playername, playerdata):
    filename = Core.prefix(playername)+".txt"
    def _save(filename, coords):
        file = open(filename, "w+")
        coords_list = list(coords)
        coords_list.sort()
        for el in coords_list:
            file.write(str(el[0])+SEP+str(el[1])+"\n")
        file.close()
    _save(Core.prefix(playername)+".txt", playerdata[0])
    _save(Core.prefix(playername)+".objectifs.txt", playerdata[1])
#
def load(playername):
    return (readcoordsfile(Core.prefix(playername)+".txt"), readcoordsfile(Core.prefix(playername)+".objectifs.txt"))
#
def loadPlanets(filename):
    file = open(filename, "r")
    planets = {}
    current = set()
    for line in file:
        try:
            Line = line.strip().split(SEP)
            (x, y) = (int(Line[0]),int(Line[1]))
            current.add((x, y))
        except ValueError as e:
            name = line.strip()
            if (name in planets):
                current = planets[name]
            else:
                current = set()
                planets[name] = current
    file.close()
    return planets
#

