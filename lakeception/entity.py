# -*- coding: utf-8 -*-

import random

from lakeception import tiles


class Entity(object):
    """
    Attributes
    pos : tuple of int, int
    tile : lakeception.tiles.Tile
    is_collidable : bool
    is_ai_controlled : bool
    """
    world = None

    def __init__(self, tile, size, pos):
        """
        Parameters
        tile: lakeception.tiles.Tile
        size: tuple of int, int
        pos : tuple of int, int
        """
        self.tile = tile
        self.size = size
        self.pos = pos

        # Set a random direction for the entity to move in
        # Currently, entities move in that direction until they can't anymore - 
        # in which case they choose a new direction and continue on their
        # journey
        self.direction = (random.randint(-1, 1), random.randint(-1, 1))

        self.is_collidable = True
        self.is_ai_controlled = True

    def set_new_direction(self):
        self.direction = (random.randint(-1, 1), random.randint(-1, 1))

    def move(self, vector):
        """
        Parameters
        vector : tuple of int, int

        Returns
        boolean
        """
        # Don't bother moving if we're not going anywhere
        if vector == (0, 0):
            return False

        # Calculate the new position
        new_pos = (self.pos[0] + vector[0], self.pos[1] + vector[1])

        # Do collision checks accounting for full entity size
        width, height = self.size
        for x in xrange(0, width):
            for y in xrange(0, height):
                check_pos = (new_pos[0] + x, new_pos[1] + y)

                # Check for collidable tiles
                tile = self.world.getTileAtPoint(check_pos)
                if tile.is_collidable:
                    return False

                # Check for collidable entities
                entity = self.world.ent_man.get_entity_at_position(check_pos)
                if entity is not None and entity is not self:
                    entity.on_collision(self)
                    return False

        # No collisions, move the entity
        self.pos = new_pos
        return True

    def on_collision(self, other):
        """
        Defines what should happen when a collision happens, from the collidee's
        perspective.

        Parameters
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
        tile = tiles.Tile("squid", "Squidward #"+str(random.randint(0, 99)), u"¤", "DE605A")
        size = (1, 1)
        self.speedBoost = 0

        super(Squid, self).__init__(tile, size, pos)

    def on_collision(self, other):
        if isinstance(other, Player):
            self.speedBoost = 0.40
            self.set_new_direction()
            self.move(self.direction)

    def on_ai_tick(self):
        # 5 % chance per tick that the squid will choose a new direction
        if random.random() < 0.05:
            self.set_new_direction()
        # 55 % chance per tick that the squid will move
        if random.random() < (0.35 + self.speedBoost):
            vector = self.direction
            # Sometimes we just move... in another direction
            if random.random() < 0.17:
                vector = (random.randint(-1, 1), random.randint(-1, 1))
                # we don't want the randomized direction to be backtracking
                if vector[0] == -self.direction[0] and \
                vector[1] == -self.direction[1]:
                    vector = self.direction
            if not self.move(vector):
                self.set_new_direction()
        if self.speedBoost:
            # decrement the speed boost
            self.speedBoost -= 0.01

class Jellyfish(NPC):
    def __init__(self, pos):
        self.names = ["Edward", ":3", "Jules", "Mircin", "Nattie", "Bento", "J", "Jarl", "Jinnie", "Jahn", "Jari", "Jurles", "Jamse", "James"]
        tile = tiles.Tile("jelly", "{} the Jellyfish".format(random.choice(self.names)), u"B", "FFA0A0")
        size = (2, 2)
        self.speedBoost = 0

        super(Jellyfish, self).__init__(tile, size, pos)

    def on_collision(self, other):
        if isinstance(other, Player):
            self.speedBoost = 0.10
            self.set_new_direction()
            self.move(self.direction)

    def on_ai_tick(self):
        # % chance per tick that the jellyfish will choose a new direction
        if random.random() < 0.45:
            self.set_new_direction()
        # % chance per tick that the squid will move
        if random.random() < (0.15 + self.speedBoost):
            vector = self.direction
            # Sometimes we just move... in another direction
            if random.random() < 0.17:
                vector = (random.randint(-1, 1), random.randint(-1, 1))
                # we don't want the randomized direction to be backtracking
                if vector[0] == -self.direction[0] and \
                vector[1] == -self.direction[1]:
                    vector = self.direction
            if not self.move(vector):
                self.set_new_direction()
        if self.speedBoost:
            # decrement the speed boost
            self.speedBoost -= 0.01

class WaterSpout(NPC):
    def __init__(self, pos):
        tile = tiles.Tile("spout", "John the Spout", u"҉", "0080FF")
        size = (1, 1)

        super(WaterSpout, self).__init__(tile, size, pos)

    def absorb(self, other_spout):
        # IT'S TIME TO GROW!  Combine the water spouts by size
        new_size = (self.size[0] + other_spout.size[0], self.size[1] + other_spout.size[1])

        self.size = new_size
        self.tile.description = "John the Super Spout"
        self.world.ent_man.ais.remove(other_spout)

        self.world.addDescription(
            "the winds seem stronger somehow...",
            color="0080FF",
        )

    def launch(self, other):
        # Send the collider to a random place in the world!
        other.pos = self.world.get_random_open_tile_position()

        if isinstance(other, Player):
            self.world.addDescription(
                "the water spout launches you through the air!",
                color="0080FF",
            )

    def on_collision(self, other):
        if isinstance(other, WaterSpout):
            self.absorb(other)
        else:
            self.launch(other)

    def on_ai_tick(self):
        # We only move a certain percentage of every tick
        if random.random() < 0.41:
            vector = self.direction
            # Sometimes we just move... in another direction
            if random.random() < 0.10:
                vector = (random.randint(-1, 1), random.randint(-1, 1))
            if not self.move(vector):
                self.set_new_direction()


NPC_TYPES = [Squid, WaterSpout, Jellyfish]


class Player(Entity):
    def __init__(self, pos, glyph, tile_color):
        """
        Parameters
        ----------
        pos : tuple if int, int
        glyph : str
        tileColor : str
        """
        tile = tiles.Tile("player", "the boat", glyph, tile_color)
        tile.elevation = "@"  # hack
        tile.biomeID = "@"    # hack

        size = (1, 1)

        super(Player, self).__init__(tile, size, pos)

        self.is_ai_controlled = False
