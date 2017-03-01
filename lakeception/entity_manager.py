# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import kdtree
import logging

from lakeception.events import EventHandler, Subscription, EVENTS, SUBEVENTS

LOGGER = logging.getLogger()


class EntityManager(object):
    u"""Handles Entities within the game, including tracking and applying certain events like movement."""
    def __init__(self, world):
        # kd trees have a fast, binary search-like lookup for items at or near a given point.  This should be a better
        # way to track sparsely distributed, arbitrarily placed mobile objects like Entities compared to scanning
        # entire near-empty grids or keeping a short list but comparing a known Entity against literally all others
        # just to find out who's in range of whom (like when drawing the viewport).
        self.entities = kdtree.create(dimensions=2)
        self.world = world

        EventHandler.subscribe(Subscription(
            EVENTS.UI_EVENT, self.on_entity_moved,
            priority=-1, is_permanent=True,
        ))

    def on_entity_moved(self, event):
        u"""
        Applies requested movement to entities without disrupting internal storage.

        :param event: 'move' event.
        """
        if hasattr(event, u'subtype') and event.subtype == SUBEVENTS.MOVE:
            entity = event.entity
            vector = event.vector

            destination = (entity.pos[0] + vector[0], entity.pos[1] + vector[1])

            if not self.world.terrain.get_at_point(destination).is_collidable:
                entity.pos = self.world.terrain.get_wrapped_point(destination)

                if not self.entities.is_balanced:
                    self.entities.rebalance()

        return False  # Don't end event; camera needs to update too

    def add(self, entity):
        u"""
        Adds the given entity to the manager at its internal position.

        :param entity: The entity to be added.
        """
        LOGGER.debug(u'Adding entity %s', type(entity))
        self.entities.add(entity)

    def remove_at(self, point):
        u"""
        Attempts to remove the entity located at the given point.  Fails silently if nothing to remove.

        :param point: (x, y) coordinate of undesired entity.
        """
        self.entities.remove(point)

    def get_at(self, point):
        u"""
        Attempts to retrieve the entity located at the given point.

        :param point: (x, y) coordinate of desired entity.
        :return: entity.Entity if present, else None.
        """
        kdnode, distance = self.entities.search_nn(point)
        nearest_neighbor = kdnode.data

        if self.world.terrain.is_equivalent_point(nearest_neighbor.pos, point):
            return nearest_neighbor
        else:
            return None

    def get_near(self, point, radius):
        u"""
        Attempts to retrieve all entities within a radius of the given point.

        :param point: (x, y) coordinate at center of target circular area.
        :param radius: Max distance from point to search within.
        :return: list of entity.Entity, possibly empty.
        """
        return [x.data for x in self.entities.search_nn_dist(point, radius)]
