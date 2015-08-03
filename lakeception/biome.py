# -*- coding: utf-8 -*-

import logging
import json
import operator
import os

from lakeception.lakeutils import getWeightedRandomChoice
from lakeception.tiles import Tile


LOGGER = logging.getLogger("lakeception.biome")
BIOMES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "biomes",
)


class Biome(object):
    def __init__(self, biomeFileName, biomeID):
        LOGGER.debug("Initializing biome: {} {}".format(biomeFileName, biomeID))

        biomeFile = json.load(open(biomeFileName, "r"))

        # Decorative name for biome
        self.name = biomeFile["name"]
        # Id which is used to reference biome in world.py
        self.id = biomeID

        # Initialize tiles
        self.tiles = {}
        for tileName, tileData in biomeFile["tiles"].iteritems():
            self.tiles[tileName] = Tile(tileName, **tileData)

        # For each initialized tile, update its list of adjacentTiles
        # so that it mirrors the now initialized tiles
        for key, tile in self.tiles.iteritems():
            if tile.adjacentTiles:
                adjacentList = []
                for tileName in tile.adjacentTiles:
                    adjacentList.append(self.tiles[tileName])
                tile.adjacentTiles = adjacentList

        # Set up how tiles occur at different elevations
        self.elevations = {}
        for elevation, weightedTiles in biomeFile["elevations"].iteritems():
            try:
                elevation = int(elevation)
            except ValueError:
                pass

            self.elevations[elevation] = []
            for tileName, occuranceWeight in weightedTiles:
                tile = self.tiles[tileName]
                self.elevations[elevation].append( (tile, occuranceWeight) )

            # Pre-sort in descending weight order.  Significantly speeds up the
            # weighted random choice algorithm used in getTileAtElevation().
            self.elevations[elevation].sort(key=operator.itemgetter(1), reverse=True)

    def getTileAtElevation(self, elevation):
        weightedTiles = self.elevations.get(elevation, self.elevations["defaultTiles"])

        weights = [x[1] for x in weightedTiles]
        choiceIndex = getWeightedRandomChoice(weights)

        tile = weightedTiles[choiceIndex][0]
        # Set up some niceties, for the different debug views on the function keys
        tile.elevation = elevation
        tile.biomeID = self.id

        return tile


# Thanks Stack Overflow!
# http://stackoverflow.com/a/3207973
def get_biome_files():
    """
    Returns
    -------
    generator of str
    """

    for filename in os.listdir(BIOMES_DIR):
        path = os.path.abspath(os.path.join(BIOMES_DIR, filename))

        # Yield file if: it is a file & its filename ends with .biome
        if os.path.isfile(path) and path.endswith(".biome"):
            yield path
