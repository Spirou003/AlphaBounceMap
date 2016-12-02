import os
import traceback
from PIL import Image, ImageColor, ImageDraw

import core

def getcolorsconfig():
    sections = core.readconfigfile("colors.ini")
    if ("example" in sections):
        del sections["example"]
    newsections = {}
    refs = []
    #interpret config file to have only integers
    for sectionname in sections:
        configs = sections[sectionname]
        newconfigs = {}
        for configname in configs:
            rgba = configs[configname].split(" ")
            ext = configs[configname].split(".")
            if (len(rgba) in [3,4]):
                if (len(rgba) == 3):
                    rgba.append(255)
                (r, g, b, a) = rgba
                try:
                    newconfigs[configname] = (int(r), int(g), int(b), int(a))
                except Exception, e:
                    #unknown format
                    pass
            elif (len(ext) == 2):
                refs.append((newconfigs, configname, ext))
            else:
                #unknown format
                pass
        newsections[sectionname] = newconfigs
    oldreflen = -1
    #resolve as many cross-references as possible
    while (len(refs) != 0 and len(refs) != oldreflen):
        i = 0
        for i in xrange(0, len(refs)):
            try:
                (newconfigs, configname, extsection, extconfig) = refs[i]
                newconfigs[configname] = newsections[extsection][extconfig]
                refs.remove((newconfigs, configname, extsection, extconfig))
                break
            except Exception, e:
                #not added yet, or impossible to add => do nothing
                pass
        oldreflen = len(refs)
    return newsections
#
def getMapFilename(playername):
    return core.prefix(playername)+".png"
#
def gridlimits(xmin, xmax, ymin, ymax, x, y):
    if (x < xmin):
        xmin = x
    elif (x > xmax):
        xmax = x
    if (y < ymin):
        ymin = y
    elif (y > ymax):
        ymax = y
    return (xmin, xmax, ymin, ymax)
#
def readcoordsfilewlimits(filename, xmin, xmax, ymin, ymax):
    file = open(filename, "r")
    list = []
    for line in file:
        Line = line.strip().split(core.SEP)
        (x, y) = (int(Line[0]),int(Line[1]))
        list.append((x, y))
        (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
    file.close()
    return (list, xmin, xmax, ymin, ymax)
#
def makeMap(playername, list, planets):
    GRID = 10
    try:
        (xmin, xmax, ymin, ymax) = (list[0][0], list[0][0], list[0][1], list[0][1])
        for el in list:
            (x, y) = el
            (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
        planetscoords = []
        for planetname in planets:
            for coords in planets[planetname]:
                (x, y) = coords
                planetscoords.append((x, y))
                (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
        (missiles, xmin, xmax, ymin, ymax) = readcoordsfilewlimits(core.datadir+"coords_missiles.txt", xmin, xmax, ymin, ymax)
        (asteroides, xmin, xmax, ymin, ymax) = readcoordsfilewlimits(core.datadir+"coords_asteroides.txt", xmin, xmax, ymin, ymax)
        lastnettoyage = []
        if (os.path.isfile(core.prefix(playername)+".lastnettoyage.txt")):
            file = open(core.prefix(playername)+".lastnettoyage.txt", "r")
            for line in file:
                if (len(line.strip()) == 0):
                    continue
                Line = ((line.strip())[1:-1]).split("] ... [")
                (x1,y1) = Line[0].split(",")
                (x2,y2) = Line[1].split("][")
                (x1,x2,y1,y2) = (int(x1),int(x2),int(y1),int(y2))
                for x in xrange(x1, x2+1):
                    for y in xrange(y1, y2+1):
                        lastnettoyage.append((x, y))
                if (x1 < xmin):
                    xmin = x1
                elif (x2 > xmax):
                    xmax = x2
                if (y1 < ymin):
                    ymin = y1
                elif (y2 > ymax):
                    ymax = y2
            file.close()
        objectifs = []
        if (os.path.isfile(core.prefix(playername)+".objectifs.txt")):
            (objectifs, xmin, xmax, ymin, ymax) = readcoordsfilewlimits(core.prefix(playername)+".objectifs.txt", xmin, xmax, ymin, ymax)
        xmin -= 5
        xmax += 5
        ymin -= 5
        ymax += 5
        image = Image.new("RGB", (xmax-xmin+1, ymax-ymin+1), "#0000aa")
        draw = ImageDraw.Draw(image)
        i = 0
        while (i < xmax):
            draw.line([(i-xmin, 0), (i-xmin, ymax-ymin)], (100, 0, 170))
            i += GRID
        i = -GRID
        while (i > xmin):
            draw.line([(i-xmin, 0), (i-xmin, ymax-ymin)], (100, 0, 170))
            i -= GRID
        i = 0
        while (i < ymax):
            draw.line([(0, i-ymin), (xmax-xmin, i-ymin)], (100, 0, 170))
            i += GRID
        i = -GRID
        while (i > ymin):
            draw.line([(0, i-ymin), (xmax-xmin, i-ymin)], (100, 0, 170))
            i -= GRID
        def drawlist(list, image, xmin, xmax, ymin, ymax, color):
            for el in list:
                (x, y) = el
                image.putpixel((x-xmin, y-ymin), color)
        drawlist(planetscoords, image, xmin, xmax, ymin, ymax, (0,0,0))
        drawlist(asteroides, image, xmin, xmax, ymin, ymax, (95,71,39))
        drawlist(missiles, image, xmin, xmax, ymin, ymax, (255,255,255))
        drawlist(lastnettoyage, image, xmin, xmax, ymin, ymax, (0,128,0))
        drawlist(objectifs, image, xmin, xmax, ymin, ymax, (0,128,0))
        for el in list:
            (x, y) = el
            color = (200,0,0)
            if (el in lastnettoyage or el in objectifs):
                color = (0,255,0)
            elif (el in planetscoords):
                color = (128,128,128)
            elif (el in asteroides):
                color = (191,142,78)
            image.putpixel((x-xmin, y-ymin), color)
        del draw
        image.save(getMapFilename(playername), "PNG")
    except Exception, e:
        traceback.print_exc()
#
