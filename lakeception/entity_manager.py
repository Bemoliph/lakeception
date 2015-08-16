# -*- coding: utf-8 -*-

from lakeception.lakeutils import dist


class EntityManager(object):
    def __init__(self, player, ai):
        self.player = player
        self.ais = ai

    def do_ai_ticks(self):
        """
        Runs AI ticks for all NPCs.
        """
        for ent in self.ais:
            if not ent.is_ai_controlled:
                continue

            ent.on_ai_tick()

    def get_entity_at_position(self, point):
        """
        Gets an entity at a given position, if one exists.

        Parameters
        ----------
        point : tuple of int, int

        Returns
        -------
        lakeception.entity.Entity or None
        """
        point_x, point_y = point

        for entity in self.ais + [self.player]:
            # Calculate collision based on entity's position AND size
            entity_x, entity_y = entity.pos
            width, height = entity.size

            dist_x = point_x - entity_x
            dist_y = point_y - entity_y

            if 0 <= dist_x < width and 0 <= dist_y < height:
                return entity

        return None

    def get_closest_entity(self, pos, entity_type=None):
        """
        Finds the closest entity to a given position, optionally of some class
        type.

        Parameters
        ----------
        pos : tuple of int, int
        entity_type : lakeception.entity.Entity

        Returns
        -------
        lakeception.entity.Entity or None
        """
        ents = self.ais + [self.player]

        # Filter the list of entities if a type was specified
        if entity_type is not None:
            ents = [
                ent
                for ent in ents
                if isinstance(ent, entity_type)
            ]

            # Return None if no entities exist of the given type
            if not ents:
                return None

        # Calculate the closest entity
        return min(
            ents,
            key=lambda ent: dist(ent.pos, pos)
        )
