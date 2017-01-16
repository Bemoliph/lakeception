# -*- coding: utf-8 -*-

import logging
import pygame
import random

from entity import Entity
from entity_manager import EntityManager
from grid import Grid
from terrain import NoiseTerrain

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
