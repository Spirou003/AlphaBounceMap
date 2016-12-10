import os
import traceback

CONFIGDIR = "config"+os.sep

def readconfigfile(filename):
    file = open(CONFIGDIR+filename, "r")
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
def oneIn(list, string):
    for name in list:
        if name in string:
            return True
    return False