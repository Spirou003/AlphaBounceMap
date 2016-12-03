import os
import traceback
from PIL import Image, ImageColor, ImageDraw

import core

colors = None
coords = {}

def getplanetcoords(planets):
    global coords
    if ("planets" in coords):
        return
    planetscoords = set()
    for planetname in planets:
        for (x, y) in planets[planetname]:
            planetscoords.add((x, y))
    coords["planets"] = planetscoords
#
def getnamefrom_coords_name_txt(filename, coords, txt):
    if (len(filename) <= len(coords)+len(txt)):
        return None
    for i in xrange(0, len(coords)):
        if (filename[i] != coords[i]):
            return None
    endfilename = filename[-len(txt):]
    for i in xrange(0, len(txt)):
        if (endfilename[i] != txt[i]):
            return None
    return filename[len(coords):len(filename)-len(txt)]
#
def loadcoords():
    patternbegin = "coords_"
    patternend = ".txt"
    filenames = os.listdir(core.datadir)
    for filename in filenames:
        name = getnamefrom_coords_name_txt(filename, "coords_", ".txt")
        if (name != None and name != "planets" and name not in coords):
            coords[name] = core.readcoordsfile(core.datadir+os.sep+filename)
#
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
                refs.append((sectionname, configname, ext))
            else:
                #unknown format
                pass
        newsections[sectionname] = newconfigs
    oldreflen = -1
    #resolve as many cross-references as possible
    while (len(refs) != 0 and len(refs) != oldreflen):
        i = 0
        oldreflen = len(refs)
        while (i < oldreflen):
            try:
                (sectionname, configname, (extsection, extconfig)) = refs[i]
                if (extsection in newsections and extconfig in newsections[extsection]):
                    newsections[sectionname][configname] = newsections[extsection][extconfig]
                    refs.pop(i)
                    i = oldreflen
            except Exception, e:
                #not added yet, or impossible to add => do nothing
                pass
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
def drawgrid(draw, xmin, xmax, ymin, ymax, GRID=10):
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
#
def drawlist(key, keylist, image, xmin, xmax, ymin, ymax, colors, explorations_copy):
    for (x, y) in keylist:
        if ((x, y) in explorations_copy):
            image.putpixel((x-xmin, y-ymin), colors["onexplore"])
            explorations_copy.remove((x, y))
        else:
            image.putpixel((x-xmin, y-ymin), colors["default"])
#
def makeMap(playername, explorations, planets):
    try:
        (xmin, xmax, ymin, ymax) = (0, 0, 0, 0)
        for el in explorations:
            (x, y) = el
            (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
        getplanetcoords(planets)
        loadcoords()
        for key in coords:
            for (x, y) in coords[key]:
                (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
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
        xmin -= 5
        xmax += 5
        ymin -= 5
        ymax += 5
        image = Image.new("RGBA", (xmax-xmin+1, ymax-ymin+1), colors["background"]["default"])
        draw = ImageDraw.Draw(image)
        drawgrid(draw, xmin, xmax, ymin, ymax)
        explorations_copy = explorations.copy()
        for key in coords:
            drawlist(key, coords[key], image, xmin, xmax, ymin, ymax, colors[key], explorations_copy)
        for el in explorations_copy:
            (x, y) = el
            color = colors["background"]["onexplore"]
            if (el in lastnettoyage):
                color = (0,255,0, 0)
            image.putpixel((x-xmin, y-ymin), color)
        del draw
        image.save(getMapFilename(playername), "PNG")
    except Exception, e:
        traceback.print_exc()
#

colors = getcolorsconfig()

