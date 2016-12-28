#coding: utf-8
import os
import traceback
import itertools

import Core, Data

from Image import EXT, getpixel, setpixel, createimage, save
from Compatibility import *

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
def loadcoords(planets):
    coords = {}
    #load planets
    planetscoords = set()
    for planetname in planets:
        for (x, y) in planets[planetname]:
            planetscoords.add((x, y))
    coords["planets"] = planetscoords
    #load other coords (missiles, asteroids and eventually others)
    patternbegin = "coords_"
    patternend = ".txt"
    filenames = os.listdir(Core.CONFIGDIR)
    for filename in filenames:
        name = getnamefrom_coords_name_txt(filename, "coords_", ".txt")
        if (name != None and name != "planets" and name not in coords):
            coords[name] = Data.readcoordsfile(Core.CONFIGDIR+filename)
    return coords
#
def getcolorsconfig(requiredkeys):
    sections = Core.readconfigfile(Core.CONFIGDIR+"colors.ini")
    #apply specific treatments for special sections
    draworder = []
    if ("display" in sections):
        draworder = sections["display"]["order"].split(" ")
        del sections["display"]
    axesgrid = 10
    if ("axes" in sections and "grid" in sections["axes"]):
        axesgrid = sections["axes"]["grid"]
        del sections["axes"]["grid"]
    newsections = {}
    refs = []
    #first pass: get colors from each line, if possible
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
                except Exception as e:
                    #unknown format
                    pass
            elif (len(ext) == 2):
                refs.append((sectionname, configname, ext))
            else:
                #unknown format
                pass
        newsections[sectionname] = newconfigs
    oldreflen = -1
    #second pass: resolve as many cross-references as possible
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
            except Exception as e:
                #not added yet, or impossible to add => do nothing
                pass
            i += 1
    #remove remaining special section if it is (I do it here to use previous useful treatment for it)
    axescolor = {"main":(255,255,0,92),"secondary":(255,255,255,32)}
    if ("axes" in newsections):
        axescolor = newsections["axes"]
        del newsections["axes"]
    axescolor["grid"] = int(axesgrid)
    #third pass: ensure each used key exists
    if ("background" not in newsections):
        bgdic = {}
        bgdic["default"] = (0,0,170,255)
        bgdic["onexplore"] = (200,0,0,255)
        bgdic["ontarget"] = (0,192,0,255)
        newsections["background"] = bgdic
    for key in requiredkeys:
        if (key not in newsections):
            newsections[key] = newsections["background"]
    #fourth pass: we need to have all config names for drawing, get missings if there are
    for key in newsections:
        if (key not in draworder):
            draworder.append(key)
    return (newsections, axescolor, draworder)
#
def getMapFilename(playername):
    return Core.prefix(playername)+EXT
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
def getgridlimits(explorations, coords, target):
    (xmin, xmax, ymin, ymax) = (0, 0, 0, 0)
    for el in explorations:
        (x, y) = el
        (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
    for key in coords:
        for (x, y) in coords[key]:
            (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
    for (x, y) in target:
        (xmin, xmax, ymin, ymax) = gridlimits(xmin, xmax, ymin, ymax, x, y)
    xmin -= 5
    xmax += 5
    ymin -= 5
    ymax += 5
    return (xmin, xmax, ymin, ymax)
#
def drawhorizontalaxes(image, xmin, xmax, ymin, ymax, GRID, color):
    G = 1
    while (G < max(abs(ymin), abs(ymax))):
        G *= GRID
        for y in xrange(ymin + (G-ymin%G)%G, ymax+1, G):
            if (y == 0):
                continue
            for k in xrange(xmin - xmin%GRID, xmax, GRID):
                for x in xrange(max(xmin, k+1), min(xmax+1, k+GRID)):
                    paintpixel(image, x-xmin, y-ymin, color)
#
def drawverticalaxes(image, xmin, xmax, ymin, ymax, GRID, color):
    G = 1
    while (G < max(abs(xmin), abs(xmax))):
        G *= GRID
        for x in xrange(xmin + (G-xmin%G)%G, xmax+1, G):
            if (x == 0):
                continue
            for k in xrange(ymin - ymin%GRID, ymax, GRID):
                for y in xrange(max(ymin, k+1), min(ymax+1, k+GRID)):
                    paintpixel(image, x-xmin, y-ymin, color)
#
def drawintersections(image, xmin, xmax, ymin, ymax, GRID, color):
    for (x, y) in itertools.product(xrange(xmin + (GRID-xmin%GRID)%GRID, xmax+1, GRID), xrange(ymin + (GRID-ymin%GRID)%GRID, ymax+1, GRID)):
        if (x != 0 and y != 0):
            (cx, cy) = (x, y)
            (axex, axey) = (0, 0)
            while (cx % GRID == 0 and cx != 0):
                axex += 1
                cx /= GRID
            while (cy % GRID == 0 and cy != 0):
                axey += 1
                cy /= GRID
            n = max(axex, axey)
            for i in xrange(0, n):
                paintpixel(image, x-xmin, y-ymin, color)
#
def drawgrid(image, axesconfig, xmin, xmax, ymin, ymax):
    GRID = axesconfig["grid"]
    for x in xrange(xmin, xmax+1):
        paintpixel(image, x-xmin, 0-ymin, axesconfig["main"])
    for y in xrange(ymin, 0):
        paintpixel(image, 0-xmin, y-ymin, axesconfig["main"])
    for y in xrange(1, ymax+1):
        paintpixel(image, 0-xmin, y-ymin, axesconfig["main"])
    drawhorizontalaxes(image, xmin, xmax, ymin, ymax, GRID, axesconfig["secondary"])
    drawverticalaxes(image, xmin, xmax, ymin, ymax, GRID, axesconfig["secondary"])
    drawintersections(image, xmin, xmax, ymin, ymax, GRID, axesconfig["secondary"])
#
def paintpixel(image, x, y, color):
    pixel = getpixel(image, x, y)
    newpixr = color[0]
    newpixg = color[1]
    newpixb = color[2]
    newpixa = color[3]
    oldpixr = pixel[0]
    oldpixg = pixel[1]
    oldpixb = pixel[2]
    oldpixa = pixel[3]
    coeff = ((255-newpixa)*oldpixa)//255
    r = (newpixr*newpixa + coeff*oldpixr)//255
    g = (newpixg*newpixa + coeff*oldpixg)//255
    b = (newpixb*newpixa + coeff*oldpixb)//255
    a = (255*255-(255-newpixa)*(255-oldpixa))//255
    setpixel(image, x, y, [r, g, b, a])
#
def drawlist(keylist, image, xmin, xmax, ymin, ymax, colors, explorations, target):
    for (x, y) in keylist:
        if ((x, y) in target):
            paintpixel(image, x-xmin, y-ymin, colors["ontarget"])
        elif ((x, y) in explorations):
            paintpixel(image, x-xmin, y-ymin, colors["onexplore"])
        else:
            paintpixel(image, x-xmin, y-ymin, colors["default"])
#
def drawmap(playername, explorations, coords, target, xmin, xmax, ymin, ymax, colors, draworder, axescolor):
    image = createimage(xmax-xmin+1, ymax-ymin+1, colors["background"]["default"])
    #draw explorations
    for (x, y) in explorations:
        color = None
        if ((x, y) in target):
            color = colors["background"]["ontarget"]
        else:
            color = colors["background"]["onexplore"]
        setpixel(image, x-xmin, y-ymin, color)
    #draw entities (planets, asteroids, ...)
    for key in draworder:
        if (key in coords):
            drawlist(coords[key], image, xmin, xmax, ymin, ymax, colors[key], explorations, target)
    #draw each remaining target
    target_copy = target.copy()
    for key in coords:
        Core.removefromlist(target_copy, coords[key])
        Core.removefromlist(target_copy, explorations)
    color = colors["background"]["ontarget"]
    for (x, y) in target_copy:
        setpixel(image, x-xmin, y-ymin, color)
    drawgrid(image, axescolor, xmin, xmax, ymin, ymax)
    save(image, getMapFilename(playername))
#
def makeMap(playername, playerdata, planets):
    explorations = playerdata[0]
    target = playerdata[1]
    coords = loadcoords(planets)
    (colors, axescolor, draworder) = getcolorsconfig(coords.keys())
    (xmin, xmax, ymin, ymax) = getgridlimits(explorations, coords, target)
    drawmap(playername, explorations, coords, target, xmin, xmax, ymin, ymax, colors, draworder, axescolor)
#

