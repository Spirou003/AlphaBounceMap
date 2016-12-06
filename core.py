import os
import traceback
from PIL import Image, ImageColor, ImageDraw

SEP = "."
datadir = "data"+os.sep

if (not os.path.isdir("saves")):
    os.mkdir("saves")
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
def readconfigfile(filename):
    file = open(datadir+os.sep+filename, "r")
    sections = {}
    currentsection = None
    for oline in file:
        line = oline.strip().lower()
        if (len(line) == 0):
            continue
        N = len(line)
        if (oline[0] == "[" and line[N-1] == "]"):
            sectionname = line[1:N-1]
            if (sectionname in sections):
                currentsection = sections[sectionname]
            else:
                currentsection = {}
                sections[sectionname] = currentsection
        elif ("=" in line):
            pos = line.find("=")
            key = line[:pos].strip()
            value = line[pos+1:].strip()
            currentsection[key] = value
        else:
            #ignore line
            pass
    return sections
#
def isforbidden(pseudo):
    return (not pseudo.isalnum())
#
def removefromlist(collection, toremove):
    for el in toremove:
        if (el in collection):
            collection.remove(el)
#
def search(x, y, explorations):
    i = 0
    for el in explorations:
        if (el[0] == x and el[1] == y):
            return i
        i += 1
    return None
#
def add(explorations, x, y):
    if ((x, y) not in explorations):
        explorations.add((x, y))
    else:
        raise ValueError("("+str(x)+" "+str(y)+") est deja explore")
#
def remove(explorations, x, y):
    if ((x, y) not in explorations):
        raise ValueError("("+str(x)+" "+str(y)+") n'est pas encore explore")
    explorations.remove((x, y))
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
def prefix(playername):
    return "saves"+os.sep+playername
#
def load(playername):
    filename = prefix(playername)+".txt"
    mode = "r+"
    if (not os.path.exists(filename)):
        mode = "w+"
    return readcoordsfile(filename, mode)
#
def loadWords(filename):
    try:
        file = open(filename, "r")
        words = []
        for line in file:
            words.append(line.strip().lower())
        file.close()
        return words
    except Exception, e:
        return []
#
def loadPlanets(filename, planets):
    file = open(filename, "r")
    planetname = ""
    for line in file:
        try:
            Line = line.strip().split(SEP)
            (x, y) = (int(Line[0]),int(Line[1]))
            planets[name].append((x, y))
        except ValueError, e:
            name = line.strip()
    file.close()
    return planets
#
def oneIn(list, string):
    for name in list:
        if name in string:
            return True
    return False
