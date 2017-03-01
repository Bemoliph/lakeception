# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import logging
import pygame
import random

from lakeception.entity import Entity
from lakeception.entity_manager import EntityManager
from lakeception.grid import Grid
from lakeception.terrain import NoiseTerrain

LOGGER = logging.getLogger()


class World(object):
    u"""Representation of the game state, excluding meta constructs like GUI."""
    def __init__(self):
        LOGGER.debug(u'Initializing World.')

        # TODO: Set this dynamically somewhere
        random.seed(42)
        tiles, dimensions = NoiseTerrain((100, 100)).generate_area()

        self.terrain = Grid(dimensions, items=tiles)
        self.entities = EntityManager(self)

        self.player = Entity(u'@', pygame.Color(u'red'), u'the boat', need_unique_surface=True)
        self.entities.add(self.player)
