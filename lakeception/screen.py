# -*- coding: utf-8 -*-

import logging
import pygame

import const

LOGGER = logging.getLogger(u'{}.screen'.format(const.PROJECT.NAME))


class Screen(object):
    def __init__(self, resolution=(640, 480)):
        LOGGER.debug(u'Initializing Screen at res=%s', resolution)
        # Set Window Title and Icon
        pygame.display.set_caption(const.PROJECT.NAME)
        pygame.display.set_icon(pygame.image.load(const.DISPLAY.ICON))
        
        # Set Window Size
        pygame.display.set_mode(resolution)
        
        # Set up framerate limiter
        self.clock = pygame.time.Clock()
        self.fps = const.DISPLAY.FPS
    
    def draw(self):
        LOGGER.debug(u'Redrawing screen.')
        
        pygame.display.flip()
        
        # Waste any remaining time to achieve desired framerate.
        time_delta = self.clock.tick(self.fps)
