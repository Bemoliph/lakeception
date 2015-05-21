# -*- coding: utf-8 -*-
import pygame

from lakeutils import hex2rgb

class Screen(object):
    def __init__(self, world, window_res, viewport_res):
        self.world = world
        
        self.background_color = hex2rgb("000000")
        self.window = pygame.display.set_mode(window_res)
        
        self.viewport_res = viewport_res
        self.viewport_tiles = [None] * (viewport_res[0] * viewport_res[1])
        
        self.sprites = {}
        self.font_face = "monospace"
        self.font_size = 24
        self.font = pygame.font.SysFont(self.font_face, self.font_size)
    
    def _charToSprite(self, char, color):
        return self.font.render(char, False, color, self.background_color)
    
    def getFontRect(self, coords, text):
        # Scalars were experimentally determined so chars touched instead of
        # overlap/gap.  Seems to work for big and small font sizes.
        width, height = self.font.size(text)
        height *= 0.9
        
        x = coords[0] * width
        y = coords[1] * height
        
        return pygame.Rect((x, y), (width, height))
    
    def getSprite(self, tile, coords):
        char = tile.getIcon()
        
        if char not in self.sprites:
            self.sprites[char] = self._charToSprite(char, tile.color)
        
        sprite_rect = self.getFontRect(coords, char)
        
        return self.sprites[char], sprite_rect
    
    def drawViewport(self):
        width, height = self.viewport_res
        
        self.world.getTilesAroundPlayer((width, height), self.viewport_tiles)
        for y in xrange(0, height):
            for x in xrange(0, width):
                tile = self.viewport_tiles[y * width + x]
                sprite, sprite_rect = self.getSprite(tile, (x,y))
                self.window.blit(sprite, sprite_rect)
    
    def draw(self):
        self.window.fill(self.background_color)
        self.drawViewport()
        
        pygame.display.update()
