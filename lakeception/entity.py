# -*- coding: utf-8 -*-

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


    def move(vector):
        """
        Parameters
        ----------
        vector : tuple of int, int

        Returns
        -------
        bool
        """
        pass


    def on_collision(self, other):
        """
        Defines what should happen when a collision happens, from the collidie's
        perspective.

        Parameters
        ----------
        other : lakeception.entity.Entity
        """
        return


    def on_ai_tick(self):
        """
        Defines what this entity does each time the AI runs.
        """
        raise NotImplementedError


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
