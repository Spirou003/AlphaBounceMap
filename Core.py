#coding: utf-8
import os
import sys

CONFIGDIR = "config"+os.sep
SAVEDIR = "saves"+os.sep

def getxrange():
    """Tricky function to have a python 2-3 compatible xrange"""
    if (sys.version_info[0] == 2):
        return xrange
    else:
        return range
#
def getraw_input():
    """Tricky function to have a python 2-3 compatible raw_input"""
    if (sys.version_info[0] == 2):
        return raw_input
    else:
        return input
#
xrange = getxrange()
raw_input = getraw_input()

def prefix(playername):
    return SAVEDIR+playername
#
def isint(string):
    if (string.isdigit()):
        return True
    else:
        return (string[0] == "-" and string[1:].isdigit())
#
def readconfigfile(filename):
    if (not os.path.exists(filename)):
        return {}
    file = open(filename, "r")
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
    file.close()
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
def loadWords(filename):
    if (os.path.exists(filename)):
        file = open(filename, "r")
        words = set()
        for line in file:
            words.add(line.strip().lower())
        file.close()
        return words
    else:
        return set()
#
def oneIn(list, string):
    for name in list:
        if name in string:
            return True
    return False
