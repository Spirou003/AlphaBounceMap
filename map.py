import os
import traceback
from PIL import Image, ImageColor, ImageDraw

import core

axescolor = None
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
    axescolor = {"main":(255,255,0,92),"secondary":(255,255,255,32)}
    if ("axes" in newsections):
        axescolor = newsections["axes"]
        del newsections["axes"]
    return (newsections, axescolor)
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
def drawgrid(image, xmin, xmax, ymin, ymax, GRID=10):
    for x in xrange(xmin, xmax):
        for y in xrange(ymin, ymax):
            (cx, cy) = (x, y)
            (axex, axey) = (0, 0)
            while (cx % GRID == 0 and cx != 0):
                axex += 1
                cx /= GRID
            while (cy % GRID == 0 and cy != 0):
                axey += 1
                cy /= GRID
            n = max(axex, axey)
            if (x == 0 or y == 0):
                putpixel(image, x-xmin, y-ymin, axescolor["main"])
            else:
                for i in xrange(0, n):
                    putpixel(image, x-xmin, y-ymin, axescolor["secondary"])
#
def putpixel(image, x, y, color):
    pixel = image.getpixel((x, y))
    newpixr = color[0]/255.
    newpixg = color[1]/255.
    newpixb = color[2]/255.
    newpixa = color[3]/255.
    oldpixr = pixel[0]/255.
    oldpixg = pixel[1]/255.
    oldpixb = pixel[2]/255.
    oldpixa = pixel[3]/255.
    coeff = (1-newpixa)*oldpixa
    r = int(255*(newpixr*newpixa + coeff*oldpixr))
    g = int(255*(newpixg*newpixa + coeff*oldpixg))
    b = int(255*(newpixb*newpixa + coeff*oldpixb))
    a = int(255*(1-(1-newpixa)*(1-oldpixa)))
    image.putpixel((x, y), (r, g, b, a))
#
def drawlist(key, keylist, image, xmin, xmax, ymin, ymax, colors, explorations, objectifs):
    for (x, y) in keylist:
        if ((x, y) in objectifs):
            putpixel(image, x-xmin, y-ymin, colors["onobjective"])
        elif ((x, y) in explorations):
            putpixel(image, x-xmin, y-ymin, colors["onexplore"])
        else:
            putpixel(image, x-xmin, y-ymin, colors["default"])
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
        objectifs = set()
        if (os.path.isfile(core.prefix(playername)+".objectifs.txt")):
            objectifs = core.readcoordsfile(core.prefix(playername)+".objectifs.txt")
        for (x, y) in objectifs:
            (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
        objectifs_copy = objectifs.copy()
        xmin -= 5
        xmax += 5
        ymin -= 5
        ymax += 5
        image = Image.new("RGBA", (xmax-xmin+1, ymax-ymin+1), colors["background"]["default"])
        #draw explorations
        for (x, y) in explorations:
            color = None
            if ((x, y) in objectifs):
                color = colors["background"]["onobjective"]
            else:
                color = colors["background"]["onexplore"]
            image.putpixel((x-xmin, y-ymin), color)
        #draw entities (planets, asteroids, ...)
        for key in coords:
            drawlist(key, coords[key], image, xmin, xmax, ymin, ymax, colors[key], explorations, objectifs)
        #mark each remaining objective
        for key in coords:
            core.removefromlist(objectifs_copy, coords[key])
        color = colors["background"]["onobjective"]
        for (x, y) in objectifs_copy:
            image.putpixel((x-xmin, y-ymin), color)
        drawgrid(image, xmin, xmax, ymin, ymax)
        image.save(getMapFilename(playername), "PNG")
    except Exception, e:
        traceback.print_exc()
#

(colors, axescolor) = getcolorsconfig()

