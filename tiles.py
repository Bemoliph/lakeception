# -*- coding: utf-8 -*-
import random

from lakeutils import hex2rgb

# Nice Tile Graveyard (nice tiles you found but don't know what to do with)
# Tile("?", "a mysterious secret", "0", "333333")
# Tile("unknown", "something unknown", "!", "B65555")

class Tile(object):
    def __init__(self, name, description, glyphs, color, collidable=False):
        self.name = name
        self.description = description
        
        self.glyph = random.choice(glyphs)
        self.allGlyphs = glyphs
        self.color = hex2rgb(color)
        
        self.collidable = collidable
        self.elevation = -1
        self.biomeID = -1
    
    def __unicode__(self):
        return self.glyph
    
    def __repr__(self):
        return self.__unicode__()

    def __hash__(self):
        return hash((self.glyph, self.color, self.biomeID, self.elevation))

    def __eq__(self, other):
        return (self.glyph, self.color, self.biomeID, self.elevation) == (other.glyph, other.color, other.biomeID, other.elevation)
