# -*- coding: utf-8 -*-
import random
import noise
from collections import Counter

from tiles import Tile
from biome import Biome
from lakeutils import getBiomeFiles

        # THUNDARAS SUGGESTION AREA
        # siren isle / sirens
        # leper beach
        # dragon roost
        # science pirate named thundara (ok this was mine)
        

class Player(object):
    def __init__(self, pos, glyph, tileColor):
        self.pos = pos
        self.tile = Tile("player", "the boat", glyph, tileColor)
        self.tile.elevation = "@" # hack
        self.tile.biomeID = "@" # hack

class World(object):
    def __init__(self, name, dimensions, debug=False):
        self.name = name
        self.biomePath = "biomes"
        self.loadBiomes()

        self.player = Player((0,0), "@", "B23530")
        # Seed the RNG so that we can debug this sucker
        random.seed(42) 
        self.descriptions = []
        self.addDescription("it was a dark and stormy night...", "FFC22C")
        
        # Smaller scale => larger homogenous areas
        self.elevationScale = 0.025
        self.biomeScale = 0.009
        
        if debug:
            self.dimensions = (5,5) # Force debug world dimensions
            self.tiles = self.generateDebugWorld()
        else:
            self.dimensions = dimensions
            self.tiles = self.generateWorld()

    # Load all the .biome files located at self.biomePath
    def loadBiomes(self):
        files = getBiomeFiles(self.biomePath)
        self.biomes = {}
        for biomeID, f in enumerate(files):
            print biomeID, f
            b = Biome(f, biomeID)
            self.biomes[biomeID] = b

    def getBiomeAtPoint(self, point):
        # Scale position and world dimensions according to biome scaling value
        x, y, worldWidth, worldHeight = [e*self.biomeScale for e in point+self.dimensions]
        noiseValue = noise.snoise2(x, y, repeatx=worldWidth, repeaty=worldHeight)
        
        # noiseValue is [-1.0, +1.0], so let's rescale and quantize it over a
        # range fitting the number of biomes currently loaded:
        biomeCount = len(self.biomes)
        biomeID = int(round((noiseValue + 1) * (biomeCount-1)/2))
        
        return self.biomes[biomeID]

    def getElevationAtPoint(self, point):
        # Scale position and world dimensions according to elevation scaling value
        x, y, worldWidth, worldHeight = [e*self.elevationScale for e in point+self.dimensions]
        noiseValue = noise.snoise2(x, y, octaves=10, repeatx=worldWidth, repeaty=worldHeight)
        
        # noiseValue is [-1.0, +1.0], so let's rescale and quantize it over [0, 20]
        elevation = int(round((noiseValue + 1) * 10))
        
        return elevation
    
    def generateWorld(self):
        # Pre-size the world array to avoid internal resizing
        worldWidth, worldHeight = self.dimensions
        tiles = [None] * (worldWidth * worldHeight)

        adjacencyDependentTiles = []
        
        # Flood the world with CREATION!
        for y in xrange(0, worldHeight):
            for x in xrange(0, worldWidth):
                point = (x, y)
                elevation = self.getElevationAtPoint(point)
                biome = self.getBiomeAtPoint(point)
                tile = biome.getTileAtElevation(elevation)
                if tile.hasAdjacencyRequirement():
                    adjacencyDependentTiles.append((tile, point))
                else:
                    tileIndex = self._pointToIndex(point, worldWidth, worldHeight)
                    tiles[tileIndex] = tile

        # Handle all the tiles with adjacency requirements
        for tile, point in adjacencyDependentTiles:
            tileX, tileY = point
            requiredTiles = []
            foundTiles = []

            for y in xrange(tileY - 1, tileY + 1):
                for x in xrange(tileX - 1, tileX + 1):
                    # This is the tile whose neighbours we are looking at;
                    # continue on to its neighbours
                    if (x, y) == point:
                        continue

                    tileIndex = self._pointToIndex((x, y), worldWidth, worldHeight)
                    adjacentTile = tiles[tileIndex]
                    foundTiles.append(adjacentTile)

                    # Check if the adjacent tile was generated (i.e. it didn't have an
                    # adjacency requirement itself), 
                    # and it is one of the tiles we require to be adjacent, 
                    # and it isn't already saved
                    if adjacentTile and adjacentTile in tile.adjacentTiles and \
                    adjacentTile not in requiredTiles:
                        requiredTiles.append(adjacentTile)

            tileIndex = self._pointToIndex(point, worldWidth, worldHeight)
            # Counter is from python's collections module; it checks if the
            # contents of the two multisets, aka containers, are the same
            if Counter(requiredTiles) == Counter(tile.adjacentTiles):
                tiles[tileIndex] = tile
            else:
                mostCommonTile = self.getMostCommonElement(foundTiles)
                if mostCommonTile:
                    tiles[tileIndex] = mostCommonTile
                else:
                    # In the event that all of the surrounding tiles have adjacency
                    # requirements, just generate the tile we're checking
                    tiles[tileIndex] = tile


        return tiles

    def getMostCommonElement(self, elements):
        data = Counter(elements)
        return data.most_common(1)[0][0]

    
    def generateDebugWorld(self):
        # Use cool pipe shapes to make positional debugging easier:
        #     ╔═══╗   (0,0)
        #     ║123║
        #     ║456║    5x5 world
        #     ║789║
        #     ╚═══╝          (4,4)        
        #grid = u"╔═══╗║123║║456║║789║╚═══╝"
        grid = u"qwertnoiseScalefgzxcvbyuiophjkl;"
        tiles = []
        for char in grid:
            t = Tile(char, char, char+char.upper(), "B23530")
            tiles.append(t)
        
        return tiles
    
    def _pointToIndex(self, point, width, height):
        x, y = point
        
        index = (y % height) * width + (x % width)
        
        return index
    
    def _indexToPoint(self, index, width):
        x = index % width
        y = index // width
        
        return (x, y)
    
    def getTileAtPoint(self, point):
        worldWidth, worldHeight = self.dimensions
        
        index = self._pointToIndex(point, worldWidth, worldHeight)
        
        return self.tiles[index]
    
    def getTilesAroundPlayer(self, size, visibleTiles):
        # Crunch some attributes of the requested area centered on the player
        width, height = size
        playerX, playerY = self.player.pos
        
        x1 = playerX - (width // 2)
        y1 = playerY - (height // 2)
        x2 = playerX + (width // 2)
        y2 = playerY + (height // 2)
        
        # Build a (wrapping) view, filling the supplied list
        index = 0
        for y in xrange(y1, y2+1):
            for x in xrange(x1, x2+1):
                visibleTiles[index] = self.getTileAtPoint((x, y))
                index += 1

    def addDescription(self, text, color="F2F2F2"):
        # The newest description is at the top of the list
        self.descriptions.insert(0, (text, color))
        # Drop the oldest message from the list
        if len(self.descriptions) > 1:
            self.descriptions.pop()
