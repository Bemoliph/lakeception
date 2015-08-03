# -*- coding: utf-8 -*-

import random

from lakeception import tiles


class Entity(object):
    """
    Attributes
    ----------
    pos : tuple of int, int
    tile : lakeception.tiles.Tile
    is_collidable : bool
    is_ai_controlled : bool
    """
    world = None

    def __init__(self, pos, tile):
        """
        Parameters
        ----------
        pos : tuple of int, int
        tile: lakeception.tiles.Tile
        """
        self.pos = pos
        self.tile = tile

        self.is_collidable = True
        self.is_ai_controlled = True


    def move(self, vector):
        """
        Parameters
        ----------
        vector : tuple of int, int

        Returns
        -------
        bool
        """
        # Don't bother moving if we're not going anywhere
        if vector == (0, 0):
            return False

        # Calculate the new position
        new_pos = (self.pos[0] + vector[0], self.pos[1] + vector[1])

        # Check for tiles, if one exists, don't move there
        tile = self.world.getTileAtPoint(new_pos)
        if tile.is_collidable:
            return False

        # Do entity collision checks
        hit = self.world.ent_man.get_entity_at_position(new_pos)
        if hit is not None:
            hit.on_collision(self)
            return False

        # No collisions, move the entity
        self.pos = new_pos
        return True


    def on_collision(self, other):
        """
        Defines what should happen when a collision happens, from the collidie's
        perspective.

        Parameters
        ----------
        other : lakeception.entity.Entity
        """
        pass


    def on_ai_tick(self):
        """
        Defines what this entity does each time the AI runs.
        """
        pass


class NPC(Entity):
    pass


class Squid(NPC):
    def __init__(self, pos):
        tile = tiles.Tile("Squidward", "squid", u"¤", "FF0000")
        super(Squid, self).__init__(pos, tile)


    def on_collision(self, other):
        print other, "->", self


    def on_ai_tick(self):
        # Try to randomly move one cell over
        vector = (random.randint(0, 1), random.randint(0, 1))
        self.move(vector)


class WaterSpout(NPC):
    def __init__(self, pos):
        tile = tiles.Tile("Spout", "spout", u"҉", "0080FF")
        super(WaterSpout, self).__init__(pos, tile)


    def on_collision(self, other):
        # Send the collider to a random place in the world!
        new_pos = self.world.get_random_open_tile_position()
        other.pos = new_pos
        self.world.addDescription(
            "a water spout launches you into the air, you land far away",
            color="0080FF",
        )


    def on_ai_tick(self):
        pass


NPC_TYPES = [Squid, WaterSpout]

class Player(Entity):
    def __init__(self, pos, glyph, tileColor):
        """
        Parameters
        ----------
        pos : tuple if int, int
        glyph : str
        tileColor : str
        """
        tile = tiles.Tile("player", "the boat", glyph, tileColor)
        tile.elevation = "@" # hack
        tile.biomeID = "@" # hack

        super(Player, self).__init__(pos, tile)

        self.is_ai_controlled = False
