#coding: utf-8

from Compatibility import *

EXT = ".bmp"

def _getimage(w, h, c=[0,0,0,0]):
    l = []
    for i in xrange(0, w):
        r = []
        for j in xrange(0, h):
            r.append(c[:])
        l.append(r)
    return l
#
def getpixel(image, x, y):
    return image[len(image)-y-1][x][:]
#
def setpixel(image, x, y, color):
    image[len(image)-y-1][x]=color[:]
#
def createimage(x, y, color=[0,0,0,0]):
    return _getimage(y, x, color)
#
def ito2chr(i):
    hi = (i & 0xff00) >> 8
    lo = i & 0x00ff
    return chr(lo) + chr(hi)
#
def ito4chr(i):
    hi = (long(i) & 0x7fff0000) >> 16
    lo = long(i) & 0x0000ffff
    return ito2chr(lo) + ito2chr(hi)

def save(image, filename):
    f = open(filename, "wb+")
    wd = len(image[0])
    ht = len(image)
    line_padding = (4 - (wd % 4)) % 4
    line_padding = wd%4
    pixelssize = ht*(wd*3 + line_padding)
    headersize = 54

    #Header
    f.write("BM")
    f.write(ito4chr(headersize + pixelssize))
    f.write(ito4chr(0))
    f.write(ito4chr(headersize))
    f.write(ito4chr(40))
    f.write(ito4chr(wd))
    f.write(ito4chr(ht))
    f.write(ito2chr(1))
    f.write(ito2chr(24))#bits per pixel
    f.write(ito4chr(0))#don't ccompress
    f.write(ito4chr(pixelssize))
    f.write(ito4chr(1))#horizontal size of pixel
    f.write(ito4chr(1))#vertical size of pixel
    f.write(ito4chr(0))
    f.write(ito4chr(0))

    #Pixels
    for row in image:
        for pixel in row:
            f.write(chr(pixel[2])+chr(pixel[1])+chr(pixel[0]))
        for i in xrange(line_padding):
            f.write(chr(0))
    f.close()
