# -*- coding: utf-8 -*-

import pygame


class PROJECT(object):
    NAME = u'Lakeception'
    DESC = u'Aww yeah, boats!'
    URL = u'https://github.com/bemoliph/lakeception'
    VERSION = u'0.0.0'
    ICON = u'icon.png'

    ASSETS_FOLDER = u'assets'


class EVENTS(object):
    # PyGame's version of SDL exposes only 9 user-defined events, listed here
    # for convenience.  Rename and use free event IDs as needed.
    WORLD_TICK = pygame.USEREVENT + 0
    WORLD_TICK_RATE = 1000
    GAME_UPDATED = pygame.USEREVENT + 1
    EVENT_3 = pygame.USEREVENT + 2
    EVENT_4 = pygame.USEREVENT + 3
    EVENT_5 = pygame.USEREVENT + 4
    EVENT_6 = pygame.USEREVENT + 5
    EVENT_7 = pygame.USEREVENT + 6
    EVENT_8 = pygame.USEREVENT + 7
    EVENT_9 = pygame.USEREVENT + 8
