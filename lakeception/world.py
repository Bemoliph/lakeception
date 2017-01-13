# -*- coding: utf-8 -*-

import logging

from grid import Grid
from texture_factory import TextureFactory

LOGGER = logging.getLogger()


class World(object):
    """Representation of the game state, excluding meta constructs like GUI."""
    def __init__(self):
        LOGGER.debug(u'Initializing World.')
        size = (5, 5)
        tiles = [
            TextureFactory.get_glyph_surface(x)
            for x in u'╔═══╗║123║║456║║789║╚═══╝'
        ]
        
        self.terrain = Grid(size, items=tiles)
