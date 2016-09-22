import os
import traceback
from PIL import Image, ImageColor, ImageDraw

SEP = "."
datadir = "data"+os.sep

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
def save(filename, list, lastentered):
    file = open(filename, "w+")
    #file.write(lastentered+"\n")
    for el in list:
        file.write(str(el[0])+SEP+str(el[1])+"\n")
    file.close()
#
def load(filename):
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
def makeMap(playername, list, planets):
    GRID = 10
    try:
        (xmin, xmax, ymin, ymax) = (list[0][0], list[0][0], list[0][1], list[0][1])
        for el in list:
            (x, y) = el
            if (x < xmin):
                xmin = x
            elif (x > xmax):
                xmax = x
            if (y < ymin):
                ymin = y
            elif (y > ymax):
                ymax = y
        file = open(datadir+"coords_missiles.txt", "r")
        missiles = []
        for line in file:
            Line = line.strip().split(SEP)
            (x, y) = (int(Line[0]),int(Line[1]))
            missiles.append((x, y))
            if (x < xmin):
                xmin = x
            elif (x > xmax):
                xmax = x
            if (y < ymin):
                ymin = y
            elif (y > ymax):
                ymax = y
        file.close()
        planetscoords = []
        for planetname in planets:
            for coords in planets[planetname]:
                (x, y) = coords
                planetscoords.append((x, y))
                if (x < xmin):
                    xmin = x
                elif (x > xmax):
                    xmax = x
                if (y < ymin):
                    ymin = y
                elif (y > ymax):
                    ymax = y
        file.close()
        file = open(datadir+"coords_asteroides.txt", "r")
        asteroides = []
        for line in file:
            Line = line.strip().split(SEP)
            (x, y) = (int(Line[0]),int(Line[1]))
            asteroides.append((x, y))
            if (x < xmin):
                xmin = x
            elif (x > xmax):
                xmax = x
            if (y < ymin):
                ymin = y
            elif (y > ymax):
                ymax = y
        file.close()
        file.close()
        file = open(datadir+"coords_lastnettoyage.txt", "r")
        lastnettoyage = []
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
        for el in planetscoords:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (0,0,0))
        for el in asteroides:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (95,71,39))
        for el in missiles:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (255,255,255))
        for el in lastnettoyage:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (0,128,0))
        for el in list:
            (x, y) = el
            color = (200,0,0)
            if (el in lastnettoyage):
                color = (0,255,0)
            elif (el in planetscoords):
                color = (128,128,128)
            elif (el in asteroides):
                color = (191,142,78)
            image.putpixel((x-xmin, y-ymin), color)
        del draw
        image.save(playername+".png", "PNG")
    except Exception, e:
        traceback.print_exc()
#