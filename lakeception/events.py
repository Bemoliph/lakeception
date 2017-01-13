# -*- coding: utf-8 -*-

import logging
import pygame

LOGGER = logging.getLogger()


class EventHandler(object):
    u"""
    Event handler that combines PyGame/SDL events and pub-sub.

    The event queue should be processed once per main game loop tick via EventHandler.pump().

    To publish an event, call EventHandler.publish() (e.g., publish(pygame.QUIT) to signal a quit).

    To subscribe to an event, pass a Subscription object to EventHandler.subscribe().  If is_permanent=False, the
    subscription will be automatically unsubscribed after the callback is executed.

    Callbacks are functions that take one argument in the form of function_name(event_object).  Optionally, a callback
    may return True to indicate the event it just processed should not propagate further to other subscribers.

    To unsubscribe from an event, pass the original Subscription object to EventHandler.unsubscribe().
    """
    # PyGame's version of SDL exposes only 8 user-defined events, listed here
    # for convenience.  Rename and use free event IDs as needed.
    WORLD_TICK = pygame.USEREVENT + 0
    WORLD_TICK_RATE = 1000
    GAME_UPDATED = pygame.USEREVENT + 1
    UI_EVENT = pygame.USEREVENT + 2
    USEREVENT_4 = pygame.USEREVENT + 3
    USEREVENT_5 = pygame.USEREVENT + 4
    USEREVENT_6 = pygame.USEREVENT + 5
    USEREVENT_7 = pygame.USEREVENT + 6
    USEREVENT_8 = pygame.USEREVENT + 7

    SUBSCRIPTIONS = {}

    @classmethod
    def pump(cls):
        u"""Processes all events in the queue.  Should be called once per main game loop tick."""
        for event in pygame.event.get():
            if cls.event_has_subscribers(event.type):
                # Execute the callbacks subscribed to this event type
                for subscription in sorted(cls.SUBSCRIPTIONS[event.type], key=lambda x: x.priority):
                    stop_propagation = subscription.callback(event)

                    # Remove one-time subscribers
                    if not subscription.is_permanent:
                        cls.unsubscribe(subscription)

                    # Callback requested to stop propagating this event
                    if stop_propagation:
                        continue

    @classmethod
    def publish(cls, event_type, payload={}):
        u"""
        Sends an event to all subscribers of that event type.

        :param event_type: See events.EventHandler and pygame.event for available event types.
        :param payload: Optional dict containing extra data.
        """
        pygame.event.post(pygame.event.Event(event_type, payload))

    @classmethod
    def subscribe(cls, subscription):
        u"""
        Subscribes to all events of the specified type, which trigger the given callback.

        :param subscription: The events.Subscription object to subscribe.
        :return: The same events.Subscription object passed in for easy chaining.
        """
        event_type = subscription.event_type

        if event_type not in cls.SUBSCRIPTIONS:
            cls.SUBSCRIPTIONS[event_type] = set()

        cls.SUBSCRIPTIONS[event_type].add(subscription)

        return subscription

    @classmethod
    def unsubscribe(cls, subscription):
        u"""
        Unsubscribe from the specified event type.

        :param subscription: The events.Subscription object to unsubscribe.
        """
        event_type = subscription.event_type

        if cls.is_subscribed(subscription):
            cls.SUBSCRIPTIONS[event_type].remove(subscription)

    @classmethod
    def event_has_subscribers(cls, event_type):
        u"""
        Determines if the given event type has any subscribers.

        :param event_type: See events.EventHandler and pygame.event for available event types.
        :return: True if event_type has subscribers, else False.
        """
        return event_type in cls.SUBSCRIPTIONS and len(cls.SUBSCRIPTIONS[event_type])

    @classmethod
    def is_subscribed(cls, subscription):
        u"""
        Determines if the Subscription is active.

        :param subscription: The events.Subscription object to check on.
        :return: True if Subscription is active, else False.
        """
        event_type = subscription.event_type
        return event_type in cls.SUBSCRIPTIONS and subscription in cls.SUBSCRIPTIONS[event_type]


class Subscription(object):
    u"""A simple container to give subscription details nice names."""
    def __init__(self, event_type, callback, priority=3, is_permanent=False):
        u"""
        Creates a new Subscription object, which must still be registered with EventHandler.subscribe().

        :param event_type: See events.EventHandler and pygame.event for available event types.
        :param callback: Reference to a function of the form function_name(event_object).  If the callback returns True,
        the event just processed will not propagate further to other subscribers.
        :param priority: Int that influences subscriber processing order.  Lower is more likely to see the event first.
        :param is_permanent:
        """
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
