# -*- coding: utf-8 -*-
import pygame
import os

from lakeutils import hex2rgb

class Screen(object):
    def __init__(self, world, windowResolution):
        self.world = world
        
        pygame.init()
        self.background_color = 0x000000
        self.window = pygame.display.set_mode(windowResolution)
        self.window.fill(self.background_color)
        
        self.sprites = {}
        self.font_face = "monospace"
        self.font_size = 20
    
    def _charToSprite(self, char, color):
        return pygame.font.SysFont(self.font_face, self.font_size).render(char, False, color)
    
    def getFontRect(self, coordinates, tile):
        # Scalars were experimentally determined so chars touched instead of
        # overlap/gap.  Seems to work for big and small font sizes.
        width = self.font_size * 0.60
        height = self.font_size * 1.10
        
        x = coordinates[0] * width
        y = coordinates[1] * height
        
        return pygame.Rect((x, y), (width, height))
    
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
