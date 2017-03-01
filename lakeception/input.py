# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import logging
import pygame

from lakeception.events import EventHandler, Subscription, EVENTS, SUBEVENTS

LOGGER = logging.getLogger()


class Input(object):
    u"""
    Input handler for the game.

    Inputs interpreted here publish events to be interpreted by subscribed objects according to their own logic.
    """
    def __init__(self, player):
        self.player = player

        repeat_delay = 35      # time between first press and start of repeats
        repeat_interval = 75   # time between each repeat
        pygame.key.set_repeat(repeat_delay, repeat_interval)

        # Listen for KEYUP and KEYDOWN events
        EventHandler.subscribe(Subscription(
            pygame.KEYUP, self.on_key,
            priority=0, is_permanent=True
        ))
        EventHandler.subscribe(Subscription(
            pygame.KEYDOWN, self.on_key,
            priority=0, is_permanent=True
        ))

        self.keybinds = {
            pygame.K_ESCAPE: self.quit,
            pygame.K_UP:     self.move,
            pygame.K_DOWN:   self.move,
            pygame.K_LEFT:   self.move,
            pygame.K_RIGHT:  self.move,
        }

    def on_key(self, event):
        u"""Routes KEYUP and KEYDOWN events to the correct function according to the key involved."""
        if event.key in self.keybinds:
            self.keybinds[event.key](event)

    def move(self, event):
        u"""Moves the player in the chosen direction."""
        if event.type == pygame.KEYDOWN:
            moves = {
                pygame.K_UP: (0, -1),   # Grid expands from top left to bottom right,
                pygame.K_DOWN: (0, 1),  # so going up and down are "reversed".
                pygame.K_LEFT: (-1, 0),
                pygame.K_RIGHT: (1, 0),
            }

            EventHandler.publish(EVENTS.UI_EVENT, SUBEVENTS.MOVE, {
                u'vector': moves[event.key],
                u'entity': self.player,
            })

            return True

    def quit(self, event):
        u"""Closes the game."""
        if event.type == pygame.KEYDOWN:
            EventHandler.publish(pygame.QUIT)
