# -*- coding: utf-8 -*-

import logging
import pygame

from screen import Screen

LOGGER = logging.getLogger()


class SurfaceFactory(object):
    u"""Handles generating and caching textures (pygame.Surface) used throughout the game."""

    surface_cache = {}
    tile_font = None
    
    @classmethod
    def get_glyph_surface(cls, glyph, color=Screen.TILE_FONT_DEFAULT_COLOR, need_unique=False):
        u"""
        Generates a square Surface containing the given glyph, centered and colored.

        By default, glyph Surfaces are cached and reused based on glyph and color.  Manipulating a shared Surface may
        have unintended side effects.  If manipulating the Surface in isolation is desired, use Surface.copy() or set
        need_unique=True when calling this function to get a new Surface that won't be cached or shared.

        :param glyph: The text to be rendered, usually a single character (a "glyph").
        :param color: The color of the glyph.
        :param need_unique: If True, a new Surface will be generated and not cached.
        :return: A square pygame.Surface containing the colored, centered glyph.
        """
        if not isinstance(color, pygame.Color):
            color = pygame.Color(color)
        
        # Use the generic RGBA tuple so whole Color objects don't pile up.
        key = (glyph, color.normalize())
        
        if need_unique or key not in cls.surface_cache:
            LOGGER.debug(u'Generating texture for %s', key)
            # Render and crop text surface
            text_surface = cls.tile_font.render(glyph, True, color)
            cropped = text_surface.subsurface(text_surface.get_bounding_rect())
            
            # Center text in standard size square tile_font
            tile = pygame.Surface(Screen.TILE_PIXEL_SIZE)
            tile.fill(Screen.BACKGROUND_COLOR)
            
            tile_width, tile_height = tile.get_size()
            cropped_width, cropped_height = cropped.get_size()
            cropped_pos = (
                (tile_width - cropped_width)/2.0,
                (tile_height - cropped_height)/2.0
            )
            
            tile.blit(cropped, cropped_pos)

            if need_unique:
                return tile
            else:
                cls.surface_cache[key] = tile
        
        return cls.surface_cache[key]
    
    @classmethod
    def init(cls):
        u"""Configures the texture factory.  Must be called after pygame.init()"""
        cls.tile_font = pygame.font.SysFont(Screen.FONT, Screen.TILE_FONT_SIZE)
