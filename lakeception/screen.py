# -*- coding: utf-8 -*-

import logging
import pygame

from const import DISPLAY, PROJECT
from lakeutils import get_abs_asset_path

LOGGER = logging.getLogger()


class Screen(object):
    u"""Handles display setup and draw calls."""

    def __init__(self, world, resolution=(640, 480), viewport_size=(20, 15)):
        LOGGER.debug(u'Initializing Screen at res=%s', resolution)
        
        # Set Window Title and Icon
        pygame.display.set_caption(PROJECT.NAME)
        pygame.display.set_icon(pygame.image.load(get_abs_asset_path(PROJECT.ICON)))
        
        # Set Window Size
        self.window = pygame.display.set_mode(resolution)
        
        # Set up frame rate limiter
        self.clock = pygame.time.Clock()
        self.fps = DISPLAY.FPS
        
        self.background_color = DISPLAY.BACKGROUND_COLOR
        
        self.world = world
        self.viewport_size = viewport_size
        self.viewport_pos = (0, 0)
    
    def move_viewport(self, top_left):
        u"""
        Moves the view of the game world to a new location, starting top left and ending bottom right.

        :param top_left: (x, y) coordinate
        """
        self.viewport_pos = top_left
    
    def draw_viewport(self):
        u"""Draws the view of the game world, including terrain and entities."""
        a, b = self.viewport_pos
        view_width, view_height = self.viewport_size
        
        # Layer 0: Draw Terrain Tiles
        for y in xrange(0, view_height):
            for x in xrange(0, view_width):
                surface = self.world.terrain.get_at_point((a + x, b + y)).surface
                surface_width, surface_height = surface.get_size()
                pos = (x * surface_width, y * surface_height)
                
                self.window.blit(surface, pos)
        
        # Layer 1: Draw Entities
    
    def draw(self):
        u"""Main draw call that draws the entire screen, inclusive of all steps."""
        LOGGER.debug(u'Redrawing screen.')
        
        self.window.fill(self.background_color)
        
        self.draw_viewport()
        
        pygame.display.update()
        
        # Waste any remaining time to achieve desired frame rate.
        time_delta = self.clock.tick(self.fps)
