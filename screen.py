# -*- coding: utf-8 -*-
import pygame
import struct
import os
from pygame.locals import *

# Utility functions ahoy
def hex2rgb(hex_str):
    return struct.unpack('BBB', hex_str.decode('hex'))

# determine the screen position of a simple surface within the grid
# def getCellRect(coordinates, screen):
#     row, column = coordinates
#     cellWidth = screen.get_width() / grid["x"]
#     cellWidth = font_size
#     return pygame.Rect(row * cellWidth,
#                        column * cellWidth,
#                        cellWidth, cellWidth)


class Screen(object):
    def __init__(self, world, resX, resY):
        self.world = world
        self.grid = {"x": world.dimensions[0], "y": world.dimensions[1]}
        
        pygame.init()
        self.resolution = (resX, resY)
        self.background_color = hex2rgb("000000")
        self.window = pygame.display.set_mode(self.resolution)
        self.window.fill(self.background_color)
        
        self.sprites = {}
        self.font_face = "monospace"
        self.font_size = 100 / self.grid["x"]
    
    def _charToSprite(self, char, color):
        return pygame.font.SysFont(self.font_face, self.font_size).render(char, False, color)
    
    def getFontRect(self, coordinates, tile):
        row, column = coordinates
        cellWidth = self.window.get_width() / self.grid["x"]
        # Rect uses Top and Left, so we need to add half of the cellWidth to get
        # to the center of the cell, and then subtract half of the e.g. tile width
        # to get the ~true~ center for displaying the character surface
        return pygame.Rect(row * cellWidth + cellWidth/2 - tile.get_width() / 2,
                           column * cellWidth + cellWidth/2 - tile.get_height() / 2,
                           cellWidth,
                           cellWidth)
    
    def getSprite(self, tile):
        char = tile.getIcon()
        
        if char not in self.sprites:
            self.sprites[char] = self._charToSprite(char, tile.color)
        
        return self.sprites[char]
    
    def draw(self, topLeft, bottomRight):
        width = bottomRight[0] - topLeft[0] + 1
        height = bottomRight[1] - topLeft[1] + 1
        
        visibleTiles = self.world.getTilesInArea(topLeft, bottomRight)
        for y in xrange(0, height):
            for x in xrange(0, width):
                tile = visibleTiles[y * width + x]
                sprite = self.getSprite(tile)
                
                sprite_pos = self.getFontRect((x, y), sprite)
                self.window.blit(sprite, sprite_pos)
        
        pygame.display.update()
