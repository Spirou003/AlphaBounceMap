import os, sys
import traceback
import core

mapwords = core.loadWords("words_map.txt")
savewords = core.loadWords("words_save.txt")
exitwords = core.loadWords("words_exit.txt")

playername = ""
if (len(sys.argv) < 2):
    playername = raw_input("Entrez votre pseudo: ")
else:
    playername = sys.argv[1]
Str = playername+".txt"
try:
    filename = Str
    list = core.load(filename)
    Str = ""
    print 'Pour desexplorer, tapez "d" devant les coordonnees "x y"'
    try:
        b = False
        while (not core.oneIn(exitwords, Str)):
            Str = raw_input("> ")
            if (core.oneIn(mapwords, Str)):
                core.makeMap(playername, list)
            elif (core.oneIn(savewords, Str)):
                core.save(filename, list, None)
            elif (core.oneIn(exitwords, Str)):
                pass
            else:
                try:
                    args = Str.strip().split(" ")
                    if (core.oneIn(args, "zone")):
                        args.remove("zone")
                        b = ('d' in args)
                        if (b):
                            args.remove("d")
                        (x1, y1, x2, y2) = args
                        x1 = int(x1)
                        y1 = int(y1)
                        x2 = int(x2)
                        y2 = int(y2)
                        (x1, x2) = (min(x1, x2), max(x1, x2))
                        (y1, y2) = (min(y1, y2), max(y1, y2))
                        for x in xrange(x1, x2+1):
                            for y in xrange(y1, y2+1):
                                try:
                                    if (b):
                                        core.remove(list, x, y)
                                    else:
                                        core.add(list, x, y)
                                except ValueError, e:
                                    print e
                                except Exception, e:
                                    print "une erreur est survenue: "+str(e)
                    else:
                        b = ('d' in args)
                        if (b):
                            args.remove("d")
                        (x, y) = args
                        x = int(x)
                        y = int(y)
                        try:
                            if (b):
                                core.remove(list, x, y)
                            else:
                                core.add(list, x, y)
                        except ValueError, e:
                            print e
                        except Exception, e:
                            print "une erreur est survenue: "+str(e)
                except Exception, e:
                    traceback.print_exc()
    except KeyboardInterrupt, e:
        core.save(filename, list, None)
    except Exception, e:
        print e
except Exception, e:
    print e