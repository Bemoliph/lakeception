# -*- coding: utf-8 -*-

import logging
import pygame

from const import DISPLAY, PROJECT
from grid import Grid

LOGGER = logging.getLogger()


class Screen(object):
    def __init__(self, world, resolution=(640, 480), viewport_size=(20, 15)):
        LOGGER.debug(u'Initializing Screen at res=%s', resolution)
        
        # Set Window Title and Icon
        pygame.display.set_caption(PROJECT.NAME)
        pygame.display.set_icon(pygame.image.load(DISPLAY.ICON))
        
        # Set Window Size
        self.window = pygame.display.set_mode(resolution)
        
        # Set up framerate limiter
        self.clock = pygame.time.Clock()
        self.fps = DISPLAY.FPS
        
        self.background_color = DISPLAY.BACKGROUND_COLOR
        
        self.world = world
        self.viewport_size = viewport_size
        self.viewport_pos = (0, 0)
    
    def move_viewport(self, top_left):
        self.viewport_pos = top_left
    
    def draw_viewport(self):
        a, b = self.viewport_pos
        view_width, view_height = self.viewport_size
        
        # Layer 0: Draw Terrain
        for y in xrange(0, view_height):
            for x in xrange(0, view_width):
                tile = self.world.terrain.get_tile_at_point((a + x, b + y))
                tile_width, tile_height = tile.get_size()
                pos = (x * tile_width, y * tile_height)
                
                self.window.blit(tile, pos)
        
        # Layer 1: Draw Entities
    
    def draw(self):
        LOGGER.debug(u'Redrawing screen.')
        
        self.window.fill(self.background_color)
        
        self.draw_viewport()
        
        pygame.display.update()
        
        # Waste any remaining time to achieve desired framerate.
        time_delta = self.clock.tick(self.fps)
