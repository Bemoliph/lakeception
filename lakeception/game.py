# -*- coding: utf-8 -*-

import logging
import pygame

from lakeception.world import World
from lakeception.screen import Screen
from lakeception.input import Input
from lakeception import audio


class Game(object):
    def __init__(self, debug=False):
        pygame.mixer.pre_init(44100, 16, 2, 4096) # setup mixer to avoid sound lag
        pygame.init()
        pygame.display.set_caption("lakeception")

        self.world = World("Test World", (100,100), debug=debug)

        if not debug:
                                           # resolution, viewport
            self.screen = Screen(self.world, (800, 475), (25, 11))
        else:
            self.screen = Screen(self.world, (800, 475), (99, 99)) # debug res

        self.input = Input(self)

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.ANIMATE = pygame.USEREVENT+0
        self.animationRate = 1 * 1000
        # Temporarily (?) disabled animations, because moving + animating was
        # an INTENSE visual experience
        # pygame.time.set_timer(self.ANIMATE, self.animationRate)

        self.updated = True
        self.quitting = False
        self.muted = False
        self.inspecting = False
        self.editing = False

        self.init_audio()


    def init_audio(self):
        try:
            pygame.mixer.init()
        except pygame.error:
            logging.warning("Unable to initialize audio")
        else:
            # From https://www.freesound.org/people/juskiddink/sounds/60507/
            # albeit a bit mixed to allow for looping
            tracks = [
                pygame.mixer.Sound(path)
                for path in audio.get_audio_files()
            ]

            # Play & loop crashing waves in the background
            # Set the volume to an unobtrusive level
            tracks[0].set_volume(0.1)
            tracks[0].play(-1)

            # Play the song at a slightly higher volume
            # import pdb; pdb.set_trace()acks[1].set_volume(0.4)
            # tracks[1].play()


    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.input.handleKey(event)
            elif event.type == self.ANIMATE:
                self.screen.draw()
                self.updated = False
            elif event.type == pygame.QUIT:
                self.quitting = True

        if self.updated:
            self.screen.draw(self.inspecting, self.editing)
            self.updated = False

        timeDelta = self.clock.tick(self.fps)
