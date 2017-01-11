# -*- coding: utf-8 -*-

import logging
import pygame

from const import DISPLAY, PROJECT
from lakeutils import hex_to_rgb, hex_to_rgba

LOGGER = logging.getLogger(u'{}.screen'.format(PROJECT.NAME))


class Screen(object):
    def __init__(self, resolution=(640, 480)):
        LOGGER.debug(u'Initializing Screen at res=%s', resolution)
        
        # Set Window Title and Icon
        pygame.display.set_caption(PROJECT.NAME)
        pygame.display.set_icon(pygame.image.load(DISPLAY.ICON))
        
        # Set Window Size
        self.window = pygame.display.set_mode(resolution)
        
        # Set up framerate limiter
        self.clock = pygame.time.Clock()
        self.fps = DISPLAY.FPS
        
        self.background_color = hex_to_rgb(DISPLAY.BACKGROUND_COLOR)
        
        # TODO: Extract to texture loader/surface generator
        self.font = pygame.font.SysFont(u'monospace', 32)
        self.set_viewport_size((8, 6))
        
        blue = pygame.image.load(u'assets/icon.png')
        tile_width, tile_height = blue.get_size()
        
        # TODO: Extract to world.terrain grid representation
        view_width, view_height = self.viewport_size
        
        self.tile_grid = [None] * (view_width * view_height)
        for y in xrange(0, view_height):
            for x in xrange(0, view_width):
                index = y * view_width + x
                
                glyph = self.get_text_surface(unichr(index + 65))
                glyph_width, glyph_height = glyph.get_size()
                tile = blue.copy()
                tile.blit(glyph, (tile_width/2 - glyph_width/2, tile_height/2 - glyph_height/2))
                
                self.tile_grid[index] = tile
    
    def get_text_surface(self, text):
        # TODO: Extract to texture loader/surface generator
        # Render text to surface and crop it
        surface = self.font.render(text, True, hex_to_rgb(0x00FF00))
        rect = surface.get_bounding_rect()
        
        return surface.subsurface(rect)
    
    def draw_viewport(self):
        # TODO: Draw in layers based on views into various world grids - 
        #   1) Draw terrain
        #   2) Draw entities
        view_width, view_height = self.viewport_size
        
        for y in xrange(0, view_height):
            for x in xrange(0, view_width):
                tile = self.tile_grid[y * view_width + x]
                tile_width, tile_height = tile.get_size()
                pos = (x * tile_width + x, y * tile_height + y)
                
                self.window.blit(tile, pos)
    
    def set_viewport_size(self, size):
        u'''Sets the width and height of the viewport in terms of tiles.'''
        if not all(type(x) == int for x in size):
            raise TypeError(u'Viewport dimensions must be of type int, gave ({}, {})'.format(*map(type, size)))
        
        self.viewport_size = size
        self.viewport_tiles = [None] * (size[0] * size[1])
    
    def draw(self):
        LOGGER.debug(u'Redrawing screen.')
        
        self.window.fill(self.background_color)
        
        self.draw_viewport()
        
        pygame.display.update()
        
        # Waste any remaining time to achieve desired framerate.
        time_delta = self.clock.tick(self.fps)
