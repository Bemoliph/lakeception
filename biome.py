# -*- coding: utf-8 -*-
import json
import operator

from lakeutils import getWeightedRandomChoice
from lakeutils import getBiomeFiles
from tiles import Tile


class Biome(object):
    def __init__(self, biomeFileName, biomeID):
        biomeFile = json.load(open(biomeFileName, "r"))
        
        # Decorative name for biome
        self.name = biomeFile["name"]
        # Id which is used to reference biome in world.py
        self.id = biomeID
        
        # Initialize tiles
        self.tiles = {}
        for tileName, tileData in biomeFile["tiles"].iteritems():
            self.tiles[tileName] = Tile(tileName, **tileData)
        
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

if __name__ == "__main__":
    testBiomePath = "biomes"
    files = getBiomeFiles(testBiomePath)
    biomes = {}
    for f in files:
        print f
        b = Biome(f)
        biomes[b.id] = b

    for biomeID in biomes:
        b = biomes[biomeID]
        print "Biome Name:", b.name
        print "Biome ID:", b.id
        
        print "Tiles:"
        for tile in b.tiles.values():
            print "  <Tile: %s, \"%s\", \"%s\", %s, col=%s, \"%s\">" % (tile.glyph, tile.name, tile.allGlyphs, tile.color, tile.collidable, tile.description)
        
        print "Elevations:"
        for elevation, weightedTiles in sorted(b.elevations.iteritems()):
            print "  %s: %s" % (elevation, weightedTiles)
        
        print "Pick some random weighted tiles at elevations:"
        import random
        for elevation in xrange(0, 20+1):
            print elevation, b.getTileAtElevation(elevation)
