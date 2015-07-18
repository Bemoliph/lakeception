# -*- coding: utf-8 -*-
import random
import noise

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
        self.elevationScale = 0.1
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
        for f in files:
            b = Biome(f)
            self.biomes[b.id] = b

    def getElevationAtPoint(self, point):
        x, y = point
        noiseValue = noise.snoise2(x*self.elevationScale, y*self.elevationScale)
        
        # noiseValue is [-1.0, +1.0], so let's rescale and quantize it over [0, 20]
        elevation = int(round((noiseValue + 1) * 10))
        
        return elevation

    def getBiomeAtPoint(self, point):
        x, y = point
        noiseValue = noise.snoise2(x*self.biomeScale, y*self.biomeScale)
        
        # noiseValue is [-1.0, +1.0], so let's rescale and quantize it over [0, 3]
        # quantization is lower for biomes since we have fewer of them than
        # elevation levels
        elevation = int(round((noiseValue + 1) * 2))
        elevation = 0 # Hack: remove this when we have more biomes
        
        return self.biomes[elevation]

    def getElevationAtPoint(self, point):
        x, y = point
        noiseValue = noise.snoise2(x*self.elevationScale, y*self.elevationScale)
        
        # noiseValue is [-1.0, +1.0], so let's rescale and quantize it over [0, 20]
        elevation = int(round((noiseValue + 1) * 10))
        
        return elevation
    
    def generateWorld(self):
        # Pre-size the world array to avoid internal resizing
        worldWidth, worldHeight = self.dimensions
        tiles = [None] * (worldWidth * worldHeight)
        
        # Flood the world with CREATION!
        for y in xrange(0, worldHeight):
            for x in xrange(0, worldWidth):
                point = (x, y)
                tileIndex = self._pointToIndex(point, worldWidth, worldHeight)
                elevation = self.getElevationAtPoint(point)
                biome = self.getBiomeAtPoint(point)
                tiles[tileIndex] = biome.getTileAtElevation(elevation)

        return tiles
    
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
