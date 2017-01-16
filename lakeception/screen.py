# -*- coding: utf-8 -*-

import logging
import pygame

from const import PROJECT
from events import EventHandler, Subscription, EVENTS, SUBEVENTS
from lakeutils import get_abs_asset_path

LOGGER = logging.getLogger()


class Screen(object):
    u"""Handles display setup and draw calls."""

    FPS = 60
    BACKGROUND_COLOR = pygame.Color(u'black')

    FONT = u'Courier New'

    TILE_PIXEL_SIZE = (16, 16)
    # Font size is in pixels, so match font height to tile height
    TILE_FONT_SIZE = TILE_PIXEL_SIZE[1]
    TILE_FONT_DEFAULT_COLOR = pygame.Color(u'white')

    def __init__(self, world, resolution=(640, 480), viewport_size=(40, 30)):
        LOGGER.debug(u'Initializing Screen at res=%s', resolution)
        
        # Set Window Title and Icon
        pygame.display.set_caption(PROJECT.NAME)
        pygame.display.set_icon(pygame.image.load(get_abs_asset_path(PROJECT.ICON)))
        
        # Set Window Size
        self.window = pygame.display.set_mode(resolution)
        
        # Set up frame rate limiter
        self.clock = pygame.time.Clock()
        
        self.world = world

        self.viewport_size = viewport_size
        self.viewport_topleft = (0, 0)
        self.viewport_center = (0, 0)
        self.move_viewport((3, 3))

        EventHandler.subscribe(Subscription(
            EVENTS.UI_EVENT, self.on_move,
            priority=0, is_permanent=True,
        ))

    def on_move(self, event):
        if hasattr(event, u'subtype') and event.subtype == SUBEVENTS.MOVE:
            self.move_viewport(event.entity.pos)

            EventHandler.publish(EVENTS.UI_EVENT, None, {
                u'is_updated': True,
            })

            return True
    
    def move_viewport(self, center):
        u"""
        Moves the view of the game world to a new location, starting top left and ending bottom right.

        :param center: (x, y) coordinate.
        """
        self.viewport_center = center

        x, y = center
        width, height = self.viewport_size
        self.viewport_topleft = (x - width // 2, y - height // 2)

    def _get_topmost_drawable_object(self, point):
        u"""
        Gets the top-most drawable object present at the point.

        Since all Surfaces have a solid-colored background, an Entity completely occludes the underlying terrain
        regardless of size or shape.  Consequently, we can safely not draw an underlying Tile wherever an Entity is.

        :param point: (x, y) coordinate.
        :return: entity.Entity if present, else tile.Tile
        """
        return self.world.entities.get_at(point) or self.world.terrain.get_at_point(point)

    def draw_viewport(self):
        u"""Draws the view of the game world, including terrain and entities."""
        # Layer 0: Terrain + Entities
        left, top = self.viewport_topleft
        view_width, view_height = self.viewport_size

        for y in xrange(0, view_height):
            for x in xrange(0, view_width):
                surface = self._get_topmost_drawable_object((left + x, top + y)).surface
                surface_width, surface_height = surface.get_size()

                pos = (x * surface_width, y * surface_height)
                self.window.blit(surface, pos)

    def draw(self):
        u"""Main draw call that draws the entire screen, inclusive of all steps."""
        LOGGER.debug(u'Redrawing screen.')
        
        self.window.fill(self.BACKGROUND_COLOR)
        
        self.draw_viewport()
        
        pygame.display.update()
        
        # Waste any remaining time to achieve desired frame rate.
        time_delta = self.clock.tick(self.FPS)
