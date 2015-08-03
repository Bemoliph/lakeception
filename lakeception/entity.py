# -*- coding: utf-8 -*-

class Entity(object):
    pass

class Player(Entity):
    def __init__(self, pos, glyph, tileColor):
        self.pos = pos
        self.tile = Tile("player", "the boat", glyph, tileColor)
        self.tile.elevation = "@" # hack
        self.tile.biomeID = "@" # hack
