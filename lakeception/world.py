# -*- coding: utf-8 -*-

import logging

from grid import Grid
from texture_factory import TextureFactory

LOGGER = logging.getLogger()


class World(object):
    def __init__(self):
        LOGGER.debug(u'Initializing World.')
        size = (5, 5)
        tiles = [
            TextureFactory.get_text_tile_surface(x)
            for x in u'╔═══╗║123║║456║║789║╚═══╝'
        ]
        
        self.terrain = Grid(size, tiles=tiles)
