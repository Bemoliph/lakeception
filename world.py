# -*- coding: utf-8 -*-
import random
import noise as noiseLib
from tiles import Tile

class Player(object):
    def __init__(self, pos, tileCharacter, tileColor):
        self.pos = pos
        self.tile = Tile("player", "the boat", "@", "B23530")

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

        # THUNDARAS SUGGESTION AREA
        # siren isle / sirens
        # leper beach
        # dragon roost
        # science pirate named thundara

        # Biomes that add flavor to the world
        self.biomes = [("cursed", "D1748F"), ("swamp", "4FDEA7"), ("pirate", "EF443A")]


    def generateWorld(self):
        # Pre-size the world array to avoid internal resizing
        worldWidth, worldHeight = self.dimensions
        tiles = [None] * (worldWidth * worldHeight)
        # Noise scale; tweak this to tweak the noise
        scale = 0.1
        # # Flood the world with CREATION!
        for y in xrange(0, worldHeight):
            for x in xrange(0, worldWidth):
                index = y*worldWidth + x
                noise = noiseLib.snoise2(x * scale, y * scale)
                if noise < 0.5:
                    tiles[index] = Tile("water", "some water", ".", "62707D")
                # Generate some more water, blank spots this time
                elif 0.5 <= noise < 0.75 :
                    tiles[index] = Tile("water", "some water", " ", "62707D")
                    # tiles[index] = Tile("unknown", "something unknown", "!", "B65555")
                # Generate a Bustling Port
                elif 0.75 <= noise <= .755:
                    tiles[index] = Tile("port", "a bustling port", "H", "B85A1C", True)
                # Generate an island
                elif 0.755 < noise <= 1:
                    tiles[index] = Tile("island", "an exotic island", "#", "F0E68C", True)

        # self.generateIslands(tiles)

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

    def addDescription(self, text, color="F2F2F2"):
        # The newest description is at the top of the list
        self.descriptions.insert(0, (text, color))
        # Drop the oldest message from the list
        if len(self.descriptions) > 1:
            self.descriptions.pop()
