# -*- coding: utf-8 -*-

import logging

from events import EventHandler, EVENTS, SUBEVENTS
from surface_factory import SurfaceFactory

LOGGER = logging.getLogger()


class Entity(object):
    def __init__(self, glyph, color, desc, pos=[0, 0], need_unique_surface=False):
        LOGGER.debug(u'Generating Entity at %s for %s', pos, (glyph, color.normalize(), desc))
        self.glyph = glyph
        self.color = color
        self.desc = desc if desc else glyph

        self.pos = list(pos)

        self.surface = SurfaceFactory.get_glyph_surface(glyph, color, need_unique_surface)

        # Announce our presence by moving in place!
        EventHandler.publish(EVENTS.UI_EVENT, SUBEVENTS.MOVE, {
            u'vector': (0, 0),
            u'entity': self,
        })

    def __getitem__(self, key):
        return self.pos.__getitem__(key)

    def __setitem__(self, key, value):
        self.pos.__setitem__(key, value)

    def __delitem__(self, key):
        self.pos.__delitem__(key)

    def __len__(self):
        return self.pos.__len__()
