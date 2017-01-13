# -*- coding: utf-8 -*-

import logging
import pygame

from surface_factory import SurfaceFactory

LOGGER = logging.getLogger()


class TileFactory(object):
    u"""Handles generating and caching Tiles used throughout the game."""
    tile_cache = {}

    @classmethod
    def get_tile(cls, glyph, color, desc, need_unique=False):
        u"""
        Generates a Tile with graphic based on given glyph and color.

        By default, Tiles are cached and reused based on glyph, color, and description.  Manipulating a shared Tile may
        have unintended side effects.  If manipulating the Tile in isolation is desired, set need_unique=True when
        calling this function to get a new Tile that won't be cached or shared.

        :param glyph: The text to graphically represent this Tile, usually a single character (a "glyph").
        :param color: The color of the glyph.
        :param desc: A short description of the Tile, to be shown when the player inspects the Tile.
        :param need_unique: If True, a new Tile will be generated and not cached.
        :return: lakeception.Tile
        """
        if not isinstance(color, pygame.Color):
            color = pygame.Color(color)

        # Use the generic RGBA tuple so whole Color objects don't pile up.
        key = (glyph, color.normalize(), desc)

        if need_unique or key not in cls.tile_cache:
            tile = Tile(glyph, color, desc)

            if need_unique:
                return tile
            else:
                cls.tile_cache[key] = tile

        return cls.tile_cache[key]


class Tile(object):
    u"""A simple terrain tile within the world."""
    def __init__(self, glyph, color, desc):
        LOGGER.debug(u'Generating Tile for %s', (glyph, color.normalize(), desc))
        self.glyph = glyph
        self.color = color
        self.desc = desc if desc else glyph

        self.surface = SurfaceFactory.get_glyph_surface(glyph, color)
