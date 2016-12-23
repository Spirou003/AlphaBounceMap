#coding: utf-8
import os
import sys

from Compatibility import *

CONFIGDIR = "config"+os.sep
SAVEDIR = "saves"+os.sep

def prefix(playername):
    """Get the prefix of all filenames used to save data's player (complete path relative to Main.py)"""
    return SAVEDIR+playername
#
def isint(string):
    """Check if a string describes an integer without try-except"""
    if (string.isdigit()):
        return True
    else:
        return (string[0] == "-" and string[1:].isdigit())
#
def readconfigfile(filename):
    """Read a structured file that describes a dictionnary of dictionnaries. Details below
    
    File contains text-blocks of this form:
    [section]
        config1 = xxxxx
        ...
        configN = yyyyy
    
    Where all names are free. Ignore leading and trealing blanks.
    If the file is not readable, return {}"""
    if (not os.path.exists(filename)):
        return {}
    file = open(filename, "r")
    sections = {}
    currentsection = None
    for oline in file:
        line = oline.strip().lower()
        comment = line.find(";")
        if (comment != -1):
            line = line[:comment]
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
def saveconfigfile(sections, filename):
    """Write dictionnary of dictionnaries to a file
    
    Output file is like this:
    [key]
        subkey1 = value1
        ...
        subkeyN = valueN
    [key2]
    ...
    
    And values are space-separated for each iterable object"""
    file = open(filename, "w+")
    for section in sections:
        file.write("["+str(section)+"]\n")
        for config in sections[section]:
            file.write("    "+str(config)+" = "+" ".join(sections[section][config])+"\n")
#
def isforbidden(pseudo):
    """Check if a string is a valid pseudo"""
    return (not pseudo.isalnum())
#
def removefromlist(collection, toremove):
    """Delete each element of collection that is contained in toremove"""
    for el in toremove:
        if (el in collection):
            collection.remove(el)
#
def oneIn(first, second):
    """Check if intersection of first and second is non-empty"""
    for name in first:
        if name in second:
            return True
    return False
