# -*- coding: utf-8 -*- 

import logging
import pygame

from const import EVENTS

LOGGER = logging.getLogger()


class Input(object):
    def __init__(self):
        repeat_delay    = 35 # time between first press and start of repeats
        repeat_interval = 75 # time between each repeat
        pygame.key.set_repeat(repeat_delay, repeat_interval)
        
        self.keybinds = {
            pygame.K_ESCAPE: self.quit,
        }
    
    def on_key(self, event):
        LOGGER.debug(u'on_key(%s)', event)
        if event.key in self.keybinds:
            self.keybinds[event.key](event)
    
    def quit(self, event):
        if event.type == pygame.KEYDOWN:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
