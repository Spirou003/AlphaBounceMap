import os
import traceback
from PIL import Image, ImageColor, ImageDraw

SEP = "."
datadir = "data"+os.sep

if (not os.path.isdir("saves")):
    os.mkdir("saves")
#
def readconfigfile(filename):
    file = open(datadir+os.sep+filename, "r")
    sections = {}
    currentsection = None
    for line in file:
        line = line.strip().lower()
        if (len(line) == 0):
            continue
        N = len(line)
        if (line[0] == "[" and line[N-1] == "]"):
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
def removefromlist(list, toremove):
    for el in toremove:
        if (el in list):
            list.remove(el)
#
def search(x, y, list):
    i = 0
    for el in list:
        if (el[0] == x and el[1] == y):
            return i
        i += 1
    return None
#
def add(list, x, y):
    if (search(x, y, list) == None):
        list.append((x, y))
        list.sort()
    else:
        raise ValueError("("+str(x)+" "+str(y)+") est deja explore")
#
def remove(list, x, y):
    index = search(x, y, list)
    if (index == None):
        raise ValueError("("+str(x)+" "+str(y)+") n'est pas encore explore")
    list.pop(index)
#
def save(playername, list, lastentered):
    filename = prefix(playername)+".txt"
    file = open(filename, "w+")
    for el in list:
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
    file = open(filename, mode)
    list = []
    for line in file:
        Line = line.strip().split(SEP)
        list.append((int(Line[0]),int(Line[1])))
    list.sort()
    file.close()
    return list
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
#
