# -*- coding: utf-8 -*-

import os
import random
import struct


def hex2rgb(hexStr):
    return struct.unpack("BBB", hexStr.decode("hex"))


def hex2rgba(hexStr, alpha):
    return hex2rgb(hexStr) + (alpha,)


def rgb2hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)

# See "Giving up the temporary list"
# http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
def getWeightedRandomChoice(orderedWeights):
    rnd = random.random() * sum(orderedWeights)
    for index, weight in enumerate(orderedWeights):
        rnd -= weight
        if rnd < 0:
            return index
