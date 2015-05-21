import random
import struct

def hex2rgb(hex_str):
    return struct.unpack('BBB', hex_str.decode('hex'))

class Tile(object):
    def __init__(self, name, description, icons, color):
        self.name = name
        self.description = description
        # A collection of characters representing the tile.
        # A random icon is chosen each frame draw for ~ambience~
        self.icons = icons
        self.color = hex2rgb(color)
    
    def getIcon(self):
        return random.choice(self.icons)
    
    def __unicode__(self):
        return self.getIcon()
    
    def __repr__(self):
        return self.__unicode__()