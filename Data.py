#coding: utf-8
import os
import traceback

from io import open
from Core import getxrange, getraw_input
xrange = getxrange()
raw_input = getraw_input()


SEP = "."
SAVEDIR = "saves"+os.sep

def printablecoords(x, y):
    return "("+str(x)+" : "+str(y)+")"
#
def prefix(playername):
    return SAVEDIR+playername
#
def readcoordsfile(filename, mode = "r"):
    file = open(filename, mode)
    coords = set()
    for line in file:
        Line = line.strip()
        if ('[' == Line[0]):
            Line = Line[1:-1].split("] ... [")
            (x1,y1) = Line[0].split(",")
            (x2,y2) = Line[1].split("][")
            (x1,x2,y1,y2) = (int(x1),int(x2),int(y1),int(y2))
            for x in xrange(x1, x2+1):
                for y in xrange(y1, y2+1):
                    coords.add((x, y))
        else:
            Line = Line.split(SEP)
            coords.add((int(Line[0]),int(Line[1])))
    file.close()
    return coords
#
def explore(playerdata, coords):
    for (x, y) in coords:
        if ((x, y) not in playerdata[0]):
            playerdata[0].add((x, y))
        else:
            print(printablecoords(x, y)+" est deja explore")
        if ((x, y) in playerdata[1]):
            playerdata[1].remove((x, y))
            print("Objectif atteint: "+printablecoords(x, y))
#
def unexplore(playerdata, coords):
    for (x, y) in coords:
        if ((x, y) not in playerdata[0]):
            print(printablecoords(x, y)+" n'est pas encore explore")
        else:
            playerdata[0].remove((x, y))
#
def save(playername, playerdata):
    filename = prefix(playername)+".txt"
    def _save(filename, coords):
        file = open(filename, "w+")
        coords_list = list(coords)
        coords_list.sort()
        for el in coords_list:
            file.write(str(el[0])+SEP+str(el[1])+"\n")
        file.close()
    _save(prefix(playername)+".txt", playerdata[0])
    _save(prefix(playername)+".objectifs.txt", playerdata[1])
#
def load(playername):
    def _load(filename):
        if (not os.path.exists(filename)):
            return set()
        else:
            return readcoordsfile(filename, "r")
    return (_load(prefix(playername)+".txt"), _load(prefix(playername)+".objectifs.txt"))
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

