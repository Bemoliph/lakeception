# -*- coding: utf-8 -*- 

import logging
import pygame

from const import EVENTS

LOGGER = logging.getLogger()


class Input(object):
    u"""
    Input handler for the game.

    Inputs interpreted here publish events to be interpreted by subscribed objects according to their own logic.
    """
    def __init__(self):
        repeat_delay = 35      # time between first press and start of repeats
        repeat_interval = 75   # time between each repeat
        pygame.key.set_repeat(repeat_delay, repeat_interval)
        
        self.keybinds = {
            pygame.K_ESCAPE: self.quit,
        }
    
    def on_key(self, event):
        u"""Routes KEYUP and KEYDOWN events to the correct function according to the key involved."""
        LOGGER.debug(u'on_key(%s)', event)
        if event.key in self.keybinds:
            self.keybinds[event.key](event)
    
    def quit(self, event):
        u"""Closes the game."""
        if event.type == pygame.KEYDOWN:
            pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
