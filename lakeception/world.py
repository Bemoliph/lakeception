# -*- coding: utf-8 -*-

import logging
import pygame

from entity import Entity
from entity_manager import EntityManager
from grid import Grid
from tile import TileFactory

LOGGER = logging.getLogger()


class World(object):
    u"""Representation of the game state, excluding meta constructs like GUI."""
    def __init__(self):
        LOGGER.debug(u'Initializing World.')
        size = (5, 5)
        tiles = [
            TileFactory.get_tile(x, pygame.Color(u'white'), u'')
            for x in u'╔═══╗║123║║456║║789║╚═══╝'
        ]

        self.terrain = Grid(size, items=tiles)
        self.ent_man = EntityManager(self)

        self.player = Entity(u'@', pygame.Color(u'red'), u'the player', need_unique_surface=True)
        self.ent_man.add(self.player)
