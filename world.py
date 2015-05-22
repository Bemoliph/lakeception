# -*- coding: utf-8 -*-
from tiles import Tile

class Player(object):
    def __init__(self, pos, tileCharacter, tileColor):
        self.pos = pos
        self.tile = Tile("player", "you, the protagonist", "@", "B23530")

class World(object):
    def __init__(self, name, dimensions, debug=False):
        self.name = name
        self.player = Player((0,0), "@", "B23530")
        # self.player_pos = (0,0) # TODO: Give player a proper representation
        
        if debug:
            self.dimensions = (5,5) # Force debug world dimensions
            self.tiles = self.generateDebugWorld()
        else:
            self.dimensions = dimensions
            self.tiles = self.generateWorld()
    
    def generateWorld(self):
        waterTile = Tile("water", "some water", "...........,~", "62707D")
        
        # Flood the world with water!
        # All elements are references to the same water tile to save memory.
        worldWidth, worldHeight = self.dimensions
        tiles = [waterTile] * (worldWidth * worldHeight)
        
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
        for y in xrange(y1, y2):
            for x in xrange(x1, x2):
                visible_tiles[index] = self.getTileAtPoint((x, y))
                index += 1
