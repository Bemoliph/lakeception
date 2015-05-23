# -*- coding: utf-8 -*-
import random

from lakeutils import hex2rgb

class Tile(object):
    def __init__(self, name, description, icons, color):
        self.name = name
        self.description = description
        # A collection of characters representing the tile.
        # A random icon is chosen each frame draw for ~ambience~
        self.icon = random.choice(icons)
        self.color = hex2rgb(color)
    
    def __unicode__(self):
        return self.getIcon()
    
    def __repr__(self):
        return self.__unicode__()
