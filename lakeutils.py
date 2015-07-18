# -*- coding: utf-8 -*-
import random
import struct
from os import listdir
from os.path import isfile, join, dirname

def hex2rgb(hexStr):
    return struct.unpack("BBB", hexStr.decode("hex"))

def hex2rgba(hexStr, alpha):
    return hex2rgb(hexStr) + (alpha,)

# See "Giving up the temporary list"
# http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
def getWeightedRandomChoice(orderedWeights):
    rnd = random.random() * sum(orderedWeights)
    for index, weight in enumerate(orderedWeights):
        rnd -= weight
        if rnd < 0:
            return index

# Thanks Stack Overflow!
# http://stackoverflow.com/a/3207973
def getBiomeFiles(biomePath):
    directory = dirname(__file__)
    biomePath = join(directory, biomePath)
    # Add file to list if: it is a file & its filename ends with .biome 
    return [join(biomePath, biomeFile) for biomeFile in listdir(biomePath) if
            isfile(join(biomePath, biomeFile)) and biomeFile.endswith(".biome")]
