# -*- coding: utf-8 -*-
import random
from tiles import Tile

class Player(object):
    def __init__(self, pos, tileCharacter, tileColor):
        self.pos = pos
        self.tile = Tile("player", "you, the protagonist", "@", "B23530")

class World(object):
    def __init__(self, name, dimensions, debug=False):
        self.name = name
        self.player = Player((0,0), "@", "B23530")
        
        if debug:
            self.dimensions = (5,5) # Force debug world dimensions
            self.tiles = self.generateDebugWorld()
        else:
            self.dimensions = dimensions
            self.tiles = self.generateWorld()
        
        self.descriptions = []
        self.addDescription("it was a dark and stormy night...", "FFC22C")

    def generateIslands(self, tiles):
        def generateFromNoise(data):
            noiseMap, noiseIterations = data
            # Fill in the tiles that we lost to the noise generation with Water
            for i in xrange(noiseIterations):
                tiles[len(tiles) - 1 - i] = Tile("water", "some water", ".", "62707D")

            # Generate the world from the noise
            for index, value in enumerate(noiseMap):
                # Generate water
                if value == 1:
                    tiles[index] = Tile("water", "some water", ".", "62707D")
                # Generate some more water, blank spots this time
                elif value == 2:
                    tiles[index] = Tile("water", "some water", " ", "62707D")
                    # tiles[index] = Tile("unknown", "something unknown", "!", "B65555")
                # Generate an island
                elif value == 3:
                    tiles[index] = Tile("island", "an exotic island", "#", "F0E68C")

        # 'iteration' keeps count of the loss stemming from repeated calls of
        # adjacentMin
        def adjacentMin(data):
            noise, iteration = data
            iteration += 1
            output = []
            for i in range(len(noise) - 1):
                output.append(min(noise[i], noise[i+1]))
            return (output, iteration)

        random.seed(0)
        noise = [random.randint(1, 3) for i in range(self.dimensions[0] * self.dimensions[1])]
        generateFromNoise(adjacentMin(adjacentMin(adjacentMin((noise, 0)))))
    
    def generateWorld(self):
        # Pre-size the world array to avoid internal resizing
        worldWidth, worldHeight = self.dimensions
        tiles = [None] * (worldWidth * worldHeight)
        
        # # Flood the world with water!
        # for y in xrange(0, worldHeight):
        #     for x in xrange(0, worldWidth):
        #         tiles[y*worldWidth + x] = Tile("water", "some water", " "*10+"."*2, "62707D")
        self.generateIslands(tiles)

        return tiles
    
    def generateDebugWorld(self):
        # Use cool pipe shapes to make positional debugging easier:
        #     ╔═══╗   (0,0)
        #     ║123║
        #     ║456║    5x5 world
        #     ║789║
        #     ╚═══╝          (4,4)        
        #grid = u"╔═══╗║123║║456║║789║╚═══╝"
        grid = u"qwertasdfgzxcvbyuiophjkl;"
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
    
    def getTilesAroundPlayer(self, size, visible_tiles):
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
                visible_tiles[index] = self.getTileAtPoint((x, y))
                index += 1

    def addDescription(self, text, color):
        # The newest description is at the top of the list
        self.descriptions.insert(0, (text, color))
        # Drop the oldest message from the list
        if len(self.descriptions) > 6:
            self.descriptions.pop()
