#coding: utf-8
import os
import traceback
import itertools

import Core
from Compatibility import *

SEP = "."

def printablecoords(x, y):
    return "("+str(x)+" : "+str(y)+")"
#
def parsecoordsline(line):
    if ('[' == line[0]):
        tmp = line[1:-1].split("] ... [")
        (x1,y1) = tmp[0].split(",")
        (x2,y2) = tmp[1].split("][")
        (x1,x2,y1,y2) = (int(x1),int(x2),int(y1),int(y2))
        return itertools.product(xrange(x1, x2+1), xrange(y1, y2+1))
    else:
        tmp = line.split(SEP)
        return [(int(tmp[0]),int(tmp[1]))]
#
def readcoordsfile(filename, mode = "r"):
    if (not os.path.exists(filename)):
        return set()
    file = open(filename, mode)
    coords = set()
    for line in file:
        Line = line.strip()
        if (len(Line) == 0):
            continue
        try:
            for (x, y) in parsecoordsline(Line):
                coords.add((x, y))
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
    mark(playerdata, coords, lambda w:str(w)+" est déjà exploré",lambda w:"Objectif atteint: "+str(w))
#
def unexplore(playerdata, coords):
    unmark(playerdata, coords, lambda w:str(w)+" n'est pas encore exploré")
#
def addtarget(playerdata, coords):
    mark((playerdata[1],[]), coords, lambda w:str(w)+" est déjà un objectif",lambda w:"Erreur: cela ne doit jamais arriver!!!")
#
def deltarget(playerdata, coords):
    unmark((playerdata[1],[]), coords, lambda w:str(w)+" n'était pas un objectif")
#
def cleartargets(playerdata):
    playerdata[1].clear()
#
def cleantargets(playerdata):
    for (x, y) in set(playerdata[1]):
        if (x, y) in playerdata[0]:
            playerdata[1].remove((x, y))
#
def save(playername, playerdata):
    def _save(filename, coords):
        tmpfilename = filename+".tmp"
        file = open(tmpfilename, "w+")
        coords_list = list(coords)
        coords_list.sort()
        for el in coords_list:
            file.write(str(el[0])+SEP+str(el[1])+"\n")
        file.close()
        os.remove(filename)
        os.rename(tmpfilename, filename)
    _save(Core.prefix(playername)+".txt", playerdata[0])
    _save(Core.prefix(playername)+".objectifs.txt", playerdata[1])
    Core.saveconfigfile(playerdata[2], Core.prefix(playername)+".infos.ini")
#
def load(playername):
    return (readcoordsfile(Core.prefix(playername)+".txt"), readcoordsfile(Core.prefix(playername)+".objectifs.txt"), Core.readconfigfile(Core.prefix(playername)+".infos.ini"))
#
def loadPlanets(filename):
    if (not os.path.exists(filename)):
        return {}
    file = open(filename, "r")
    planets = {}
    current = set()
    for line in file:
        Line = line.strip()
        if (len(Line) == 0):
            continue
        if (Line[0] == "<" and Line[-1] == ">"):
            name = line.strip()[1:-1]
            if (name in planets):
                current = planets[name]
            else:
                current = set()
                planets[name] = current
        else:
            try:
                for (x, y) in parsecoordsline(Line):
                    current.add((x, y))
            except Exception as e:
                print(str(filename)+": format invalide: "+line)
    file.close()
    return planets
#
def getTerreCoords(x, y):
    coords = set()
    for (X, Y) in itertools.product(xrange(x-3,x+3), xrange(y-3, y+3)):
        coords.add((X, Y))
    coords.remove((x-3, y-3))
    coords.remove((x-3, y+2))
    coords.remove((x+2, y+2))
    coords.remove((x+2, y-3))
    return coords
#
