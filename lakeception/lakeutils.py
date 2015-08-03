# -*- coding: utf-8 -*-

from math import sqrt
import os
import random
import struct


def hex2rgb(hexStr):
    return struct.unpack("BBB", hexStr.decode("hex"))


def hex2rgba(hexStr, alpha):
    return hex2rgb(hexStr) + (alpha,)


def rgb2hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


def dist(pos_a, pos_b):
    return sqrt(
        (pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2
    )

# See "Giving up the temporary list"
# http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
def getWeightedRandomChoice(orderedWeights):
    rnd = random.random() * sum(orderedWeights)
    for index, weight in enumerate(orderedWeights):
        rnd -= weight
        if rnd < 0:
            return index
