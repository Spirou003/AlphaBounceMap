from PIL import Image, ImageColor
import os
import traceback

SEP = "."

mode = "r"
Str = raw_input("Entrez votre pseudo: ")
if (os.path.exists(Str+".txt")):
    try:
        file = open(Str+".txt", mode)
        list = []
        for line in file:
            Line = line.strip().split(SEP)
            list.append((int(Line[0]),int(Line[1])))
        file.close()
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
        file = open("coords.missiles", mode)
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
        file = open("coords.planets", mode)
        planets = []
        for line in file:
            Line = line.strip().split(SEP)
            (x, y) = (int(Line[0]),int(Line[1]))
            planets.append((x, y))
            if (x < xmin):
                xmin = x
            elif (x > xmax):
                xmax = x
            if (y < ymin):
                ymin = y
            elif (y > ymax):
                ymax = y
        file.close()
        file = open("coords.asteroides", mode)
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
        file = open("coords.lastnettoyage", mode)
        lastnettoyage = []
        for line in file:
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
        for el in missiles:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (255,255,255))
        for el in planets:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (0,0,0))
        for el in asteroides:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (95,71,39))
        for el in lastnettoyage:
            (x, y) = el
            image.putpixel((x-xmin, y-ymin), (0,128,0))
        for el in list:
            (x, y) = el
            color = (200,0,0)
            if (el in lastnettoyage):
                color = (0,255,0)
            elif (el in planets):
                color = (128,128,128)
            elif (el in asteroides):
                color = (191,142,78)
            image.putpixel((x-xmin, y-ymin), color)
        image.save(Str+".png", "PNG")
    except Exception, e:
        traceback.print_exc()