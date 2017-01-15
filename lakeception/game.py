# -*- coding: utf-8 -*-

import logging
import pygame

from audio import Audio
from events import EventHandler, Subscription, EVENTS
from input import Input
from screen import Screen
from surface_factory import SurfaceFactory
from world import World

LOGGER = logging.getLogger()


class Game(object):
    u"""Central point for initializing all other game components and host of main game loop."""
    def __init__(self):
        LOGGER.debug(u'Initializing Game.')
        
        # When True, the game will close. Set via pygame.QUIT
        self.is_quitting = False
        # When True, the screen will redraw. Set via const.EVENTS.GAME_UPDATED
        self.is_updated = True
        self.is_running = False
        
        # Set up audio BEFORE initializing pygame.
        Audio.pre_init()
        
        pygame.init()
        
        # Set up TextureFactory AFTER initializing pygame.
        SurfaceFactory.init()
        
        self.world = World()
        self.audio = Audio()
        self.input = Input(self.world.player)
        self.screen = Screen(self.world)

        # Listen for changes to game or UI state so we know when to draw
        EventHandler.subscribe(Subscription(
            EVENTS.UI_EVENT, self.on_updated,
            priority=0, is_permanent=True,
        ))

        # Listen for quits to handle them gracefully
        EventHandler.subscribe(Subscription(
            pygame.QUIT, self.on_quit,
            priority=0, is_permanent=True,
        ))
    
    def start(self):
        u"""Initiates the main game loop, starting the game."""
        if not self.is_running:
            LOGGER.debug(u'Starting main game loop.')
            self.is_running = True

            # Set a generic, repeating event to represent "time" passing in-world.
            pygame.time.set_timer(
                EVENTS.WORLD_TICK,
                EventHandler.WORLD_TICK_RATE
            )

            # Main game loop!
            while not self.is_quitting:
                self.tick()

            LOGGER.debug(u'Exiting main game loop.')
            self.is_running = False
            # Fall-through here ends the game naturally
    
    def tick(self):
        u"""Main game loop logic.  Called once per iteration of main game loop."""
        # Process any events sent since last tick:
        EventHandler.pump()

        # Redraw the screen as necessary:
        if self.is_updated:
            self.screen.draw()
            self.is_updated = False

    def on_updated(self, event):
        if hasattr(event, 'is_updated'):
            self.is_updated = event.is_updated

            return True
    
    def on_quit(self, event):
        LOGGER.debug(u'Quit requested by user.')
        # TODO: Save game state, other tear-down.
        
        # Signal to main loop that it should end.
        self.is_quitting = True
