import os
import traceback

import Core

SEP = "."
SAVEDIR = "saves"+os.sep

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
def explore(explorations, x, y):
    if ((x, y) not in explorations):
        explorations.add((x, y))
    else:
        raise ValueError("("+str(x)+" "+str(y)+") est deja explore")
#
def unexplore(explorations, x, y):
    if ((x, y) not in explorations):
        raise ValueError("("+str(x)+" "+str(y)+") n'est pas encore explore")
    explorations.remove((x, y))
#
def explorezone(explorations, x1, y1, x2, y2):    
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    for x in xrange(x1, x2+1):
        for y in xrange(y1, y2+1):
            try:
                explore(explorations, x, y)
            except ValueError, e:
                print e
            except Exception, e:
                traceback.print_exc()
#
def unexplorezone(explorations, x1, y1, x2, y2):
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    for x in xrange(x1, x2+1):
        for y in xrange(y1, y2+1):
            try:
                unexplore(explorations, x, y)
            except ValueError, e:
                print e
            except Exception, e:
                traceback.print_exc()
#
def exploreplanet(explorations, planets, planetname):
    for (x, y) in planets[planetname]:
        try:
            explore(explorations, x, y)
        except ValueError, e:
            print e
        except Exception, e:
            traceback.print_exc()
#
def unexploreplanet(explorations, planets, planetname):
    for (x, y) in planets[planetname]:
        try:
            unexplore(explorations, x, y)
        except ValueError, e:
            print e
        except Exception, e:
            traceback.print_exc()
#
def save(playername, explorations, lastentered):
    filename = prefix(playername)+".txt"
    file = open(filename, "w+")
    explorations_list = list(explorations)
    explorations_list.sort()
    for el in explorations_list:
        file.write(str(el[0])+SEP+str(el[1])+"\n")
    file.close()
#
def load(playername):
    filename = prefix(playername)+".txt"
    mode = "r+"
    if (not os.path.exists(filename)):
        mode = "w+"
    return readcoordsfile(filename, mode)
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
        except ValueError, e:
            name = line.strip()
            if (name in planets):
                current = planets[name]
            else:
                current = set()
                planets[name] = current
    file.close()
    return planets
#

