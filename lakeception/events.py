# -*- coding: utf-8 -*-

import logging
import pygame

LOGGER = logging.getLogger()


class EventHandler(object):
    """
    Event handler that combines PyGame/SDL events and pub-sub.

    """
    # PyGame's version of SDL exposes only 9 user-defined events, listed here
    # for convenience.  Rename and use free event IDs as needed.
    WORLD_TICK = pygame.USEREVENT + 0
    WORLD_TICK_RATE = 1000
    GAME_UPDATED = pygame.USEREVENT + 1
    USEREVENT_3 = pygame.USEREVENT + 2
    USEREVENT_4 = pygame.USEREVENT + 3
    USEREVENT_5 = pygame.USEREVENT + 4
    USEREVENT_6 = pygame.USEREVENT + 5
    USEREVENT_7 = pygame.USEREVENT + 6
    USEREVENT_8 = pygame.USEREVENT + 7
    USEREVENT_9 = pygame.USEREVENT + 8

    SUBSCRIPTIONS = {}

    @classmethod
    def pump(cls):
        for event in pygame.event.get():
            if cls.event_has_subscriptions(event.type):
                # Execute the callbacks subscribed to this event type
                for subscription in cls.SUBSCRIPTIONS[event.type]:
                    stop_propagation = subscription.callback(event)

                    # Remove one-time subscribers
                    if not subscription.is_permanent:
                        cls.unsubscribe(subscription)

                    # Callback requested to stop propagating this event
                    if stop_propagation:
                        continue

    @classmethod
    def publish(cls, event_type, payload={}):
        pygame.event.post(pygame.event.Event(event_type, payload))

    @classmethod
    def subscribe(cls, subscription):
        event_type = subscription.event_type

        if event_type not in cls.SUBSCRIPTIONS:
            cls.SUBSCRIPTIONS[event_type] = set()

        cls.SUBSCRIPTIONS[event_type].add(subscription)

    @classmethod
    def unsubscribe(cls, subscription):
        event_type = subscription.event_type

        if cls.is_subscribed(subscription):
            cls.SUBSCRIPTIONS[event_type].remove(subscription)

    @classmethod
    def event_has_subscriptions(cls, event_type):
        return event_type in cls.SUBSCRIPTIONS and len(cls.SUBSCRIPTIONS[event_type])

    @classmethod
    def is_subscribed(cls, subscription):
        event_type = subscription.event_type
        return event_type in cls.SUBSCRIPTIONS and subscription in cls.SUBSCRIPTIONS[event_type]


class Subscription(object):
    def __init__(self, event_type, callback, priority, is_permanent=False):
        self.event_type = event_type
        self.callback = callback
        self.priority = priority
        self.is_permanent = is_permanent

    def __str__(self):
        return '<{}.{}: {} -> {}.{}, Priority: {}, Permanent: {}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.event_type,
            self.callback.__module__,
            self.callback.__name__,
            self.priority,
            self.is_permanent,
        )

    def __unicode__(self):
        return unicode(self.__str__())

    def __eq__(self, other):
        return (self.event_type, self.callback, self.priority, self.is_permanent) == \
               (other.event_type, other.callback, other.priority, other.is_permanent)

    def __hash__(self):
        return hash((self.event_type, self.callback, self.priority, self.is_permanent))
