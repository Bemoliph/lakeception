# -*- coding: utf-8 -*-

import logging
import pygame

from const import DISPLAY

LOGGER = logging.getLogger()


class TextureFactory(object):
    surface_cache = {}
    tile_font = None
    
    @classmethod
    def get_text_tile_surface(cls, text, color=DISPLAY.TILE_FONT_COLOR):
        if not isinstance(color, pygame.Color):
            color = pygame.Color(color)
        
        # Use the generic RGBA tuple so whole Color objects don't pile up.
        key = (text, color.normalize())
        
        if key not in cls.surface_cache:
            # Render and crop text surface
            text_surface = cls.tile_font.render(text, True, color)
            cropped = text_surface.subsurface(text_surface.get_bounding_rect())
            
            # Center text in standard size square tile_font
            tile = pygame.Surface(DISPLAY.TILE_PIXEL_SIZE)
            tile.fill(DISPLAY.BACKGROUND_COLOR)
            
            tile_width, tile_height = tile.get_size()
            cropped_width, cropped_height = cropped.get_size()
            cropped_pos = (
                (tile_width- cropped_width)/2.0,
                (tile_height - cropped_height)/2.0
            )
            
            tile.blit(cropped, cropped_pos)
            
            cls.surface_cache[key] = tile
        
        return cls.surface_cache[key]
    
    @classmethod
    def init(cls):
        cls.tile_font = pygame.font.SysFont(DISPLAY.FONT, DISPLAY.TILE_FONT_SIZE)
