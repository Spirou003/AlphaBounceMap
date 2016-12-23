#coding: utf-8
import sys

"""
Module used to define all common functions that may differ between Python 2 and in Python 3
I don't want to use modules like futurize because the program have to work:
- with Pytho 2 and Python 3
- without installing any extra-module
PIL module actually used by Map.py should be removed
"""

xrange = xrange if (sys.version_info[0] == 2) else range
raw_input = raw_input if (sys.version_info[0] == 2) else input

"""
We need accents for french => need UTF-8
Python 2: default ANSI => need print(string.decode("utf-8")) for accents
Python 3: UTF-8 default => print(string) is ok for accents
We can't use a ternary form like previous for this since in Python 2, print is a keyword
"""
def printf2(s):
    print(s.decode("utf-8"))
def printf3(s):
    print(s)
printf = printf2 if (sys.version_info[0] == 2) else printf3
