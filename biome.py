# -*- coding: utf-8 -*-
import json
import operator

from lakeutils import getWeightedRandomChoice
from tiles import Tile

class Biome(object):
    def __init__(self, biomeFileName):
        biomeFile = json.load(open(biomeFileName, "r"))
        
        self.name = biomeFile["name"]
        
        # Initialize tiles
        self.tiles = {}
        for tileName, tileData in biomeFile["tiles"].iteritems():
            self.tiles[tileName] = Tile(tileName, **tileData)
        
        # Set up how tiles occur at different heights
        self.elevations = {}
        for height, weightedTiles in biomeFile["elevations"].iteritems():
            try:
                height = int(height)
            except ValueError:
                pass
            
            self.elevations[height] = []
            for tileName, occuranceWeight in weightedTiles:
                tile = self.tiles[tileName]
                self.elevations[height].append( (tile, occuranceWeight) )
            
            # Pre-sort in descending weight order.  Significantly speeds up the
            # weighted random choice algorithm used in getTileAtElevation().
            self.elevations[height].sort(key=operator.itemgetter(1), reverse=True)
    
    def getTileAtElevation(self, height):
        weightedTiles = self.elevations.get(height, self.elevations["defaultTiles"])
        
        weights = [x[1] for x in weightedTiles]
        choiceIndex = getWeightedRandomChoice(weights)
        
        return weightedTiles[choiceIndex][0]

if __name__ == "__main__":
    testBiomeFileName = r"E:\Users\User\Desktop\Category\jams\lakeception\test.biome"
    b = Biome(testBiomeFileName)
    
    print "Biome Name:", b.name
    
    print "Tiles:"
    for tile in b.tiles.values():
        print "  <Tile: %s, \"%s\", \"%s\", %s, col=%s, \"%s\">" % (tile.glyph, tile.name, tile.allGlyphs, tile.color, tile.collidable, tile.description)
    
    print "Elevations:"
    for height, weightedTiles in sorted(b.elevations.iteritems()):
        print "  %s: %s" % (height, weightedTiles)
    
    print "Pick some random weighted tiles at heights:"
    import random
    for height in xrange(0, 20+1):
        print height, b.getTileAtElevation(height)