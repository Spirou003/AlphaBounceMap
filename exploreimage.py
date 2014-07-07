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
        for el in list:
            (x, y) = el
            if (el in planets):
                image.putpixel((x-xmin, y-ymin), (128,128,128))
            else:
                image.putpixel((x-xmin, y-ymin), (200,0,0))
        image.save(Str+".png", "PNG")
    except Exception, e:
        traceback.print_exc()