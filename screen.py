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
        resolution = (resX, resY)
        self.window = pygame.display.set_mode(resolution)
        bg_color = hex2rgb("000000")
        self.window.fill(bg_color)

        # LE GLOBALS 
        # initially haxed & adapted from http://stackoverflow.com/a/19120806
        # self.window horizontal res / grid width
        font_size =  100 / self.grid["x"]
        current_position = [0, 1]
        
        charset = u"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~.*╔╗╚╝║═123456789"
        gray = hex2rgb("B23530")
        self.charmap = {char:self._charToImage(char, "monospace", font_size, gray) for char in charset}
        
        player_color = hex2rgb("7F3333")
        self.player = self._charToImage("@", "monospace", font_size, player_color)
    
    def _charToImage(self, char, font, font_size, color):
        return pygame.font.SysFont(font, font_size).render(char, False, color)
    
    def getFontRect(self, coordinates, tile):
        row, column = coordinates
        cellWidth = self.window.get_width() / self.grid["x"]
        # Rect uses Top and Left, so we need to add half of the cellWidth to get
        # to the center of the cell, and then subtract half of the e.g. tile width
        # to get the ~true~ center for displaying the character surface
        return pygame.Rect(row * cellWidth + cellWidth/2 - tile.get_width() / 2,
                           column * cellWidth + cellWidth/2 - tile.get_height() / 2,
                           cellWidth, cellWidth)
    
    def draw(self, topLeft, bottomRight):
        width = bottomRight[0] - topLeft[0] + 1
        height = bottomRight[1] - topLeft[1] + 1
        visibleTiles = self.world.getTilesInArea(topLeft, bottomRight)

        # draw.py stuff
        # fill the entire screen with the background color
        # self.canvas.fill(bg_color)
        # isOdd = False
        # for row in xrange(grid["x"]):
        #     for column in xrange(grid["y"]):
        #         pos = get_cell_rect((row, column), screen)
        #         # debug-draw a filled rectangle every odd tile
        #         if not isOdd:
        #             # screen.fill((255, 0, 0), pos)
        #             isOdd = True
        #         else:
        #             isOdd = False

        #         # get the screen position for the tile
        #         font_pos = get_font_rect((row, column), screen, tile)
        #         # draw the tile
        #         screen.blit(tile, font_pos)

        
        for row in xrange(0, height):
            rowIndex = row*width
            rowIcons = visibleTiles[rowIndex : rowIndex+width]
            for column, icon in enumerate(rowIcons): 
                # Get the corresponding image for the icon
                tile = self.charmap[unicode(icon)]
                # Find the screen position for the world cell
                font_pos = self.getFontRect((row, column), tile)
                # Write the tile to the screen
                self.window.blit(tile, font_pos)

        pygame.display.update()
