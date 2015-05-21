# -*- coding: utf-8 -*-
from tiles import Tile

class World(object):
    def __init__(self, name, dimensions, debug=False):
        self.name = name
        
        if debug:
            self.dimensions = (5, 5) # Force debug world dimensions
            self.tiles = self.generateDebugWorld()
        else:
            self.dimensions = dimensions
            self.tiles = self.generateWorld()
    
    def generateWorld(self):
        waterTile = Tile("water", "some water", "...........,~", "3035B2")
        
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
        grid = u"╔═══╗║123║║456║║789║╚═══╝"
        tiles = []
        for char in grid:
            t = Tile(char, char, char, "B23530")
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
    
    def getTilesInArea(self, topLeft, bottomRight):
        # Crunch some attributes of the requested area
        x1, y1 = topLeft
        x2, y2 = bottomRight
        
        areaWidth = x2-x1+1
        areaHeight = y2-y1+1
        area = areaWidth * areaHeight
        
        # Build a (wrapping) view of the requested area
        areaTiles = [None] * area # Pre-size the list to avoid Python internally resizing/copying needlessly
        index = 0
        for y in xrange(y1, y2+1):
            for x in xrange(x1, x2+1):
                areaTiles[index] = self.getTileAtPoint((x, y))
                index += 1
        
        return areaTiles

if __name__ == "__main__":
    w = World("Test World", (5,5), debug=True)
    print w.getTilesInArea((-1,-1), (4,3))
