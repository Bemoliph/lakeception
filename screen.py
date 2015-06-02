# -*- coding: utf-8 -*-
import pygame

from lakeutils import hex2rgb
from lakeutils import hex2rgba

from tiles import Tile

class Screen(object):
    def __init__(self, world, window_res, viewport_res):
        self.world = world

        self.background_color = hex2rgb("0E0E0E")
        self.window = pygame.display.set_mode(window_res)
        
        self.viewport_res = viewport_res
        # viewport_res has to be square & odd for viewport_center to be correct
        self.viewport_center = (viewport_res[0] // 2, viewport_res[1] // 2)
        self.viewport_tiles = [None] * (viewport_res[0] * viewport_res[1])
        
        self.sprites = {}
        self.font_face = "monospace"
        self.font_size = window_res[0] / self.viewport_res[0]
        self.font = pygame.font.SysFont(self.font_face, self.font_size)
        self.cursor = (0, 0)
        self.cursor_surface = pygame.Surface((self.font_size, self.font_size), pygame.SRCALPHA, 32)
        self.cursor_surface.fill(hex2rgba("F2F2F2", 50))

        self.descriptionFont = pygame.font.SysFont("monospace", 15)
    
    def _charToSprite(self, char, color):
        return self.font.render(char, False, color, self.background_color)
    
    def getFontRect(self, coords, text):
        # Scalars were experimentally determined so chars touched instead of
        # overlap/gap.  Seems to work for big and small font sizes.
        width, height = self.font.size(text)
        height *= 0.85
        width *= 1.75
        
        x = coords[0] * width
        y = coords[1] * height
        
        return pygame.Rect((x, y), (width, height))
    
    def getSprite(self, tile, coords):
        char = tile.icon
        
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

    def drawPlayer(self):
        player = self.world.player
        sprite, sprite_rect = self.getSprite(player.tile, self.viewport_center)
        self.window.blit(sprite, sprite_rect)

    def drawInspectionCursor(self):
        player_pos = self.world.player.pos
        # world_pos = player position + cursor position
        world_pos = (player_pos[0] + self.cursor[0], player_pos[1] + self.cursor[1])
        # Screen position differs from world position, as we're drawing with
        # respect to the viewport
        screen_pos = (self.viewport_center[0] + self.cursor[0], self.viewport_center[1] + self.cursor[1])
        screen_pos = self.getFontRect(screen_pos, "#")

        # If the cursor is centered in the viewport => it's hovering above the player
        if self.cursor == (0, 0):
            # Get the player tile
            tile = self.world.player.tile
        else:
            tile = self.world.getTileAtPoint(world_pos)
        self.world.addDescription(tile.description)

        # Magic numbers => center the cursor on the tile it's hovering over, kind of
        self.window.blit(self.cursor_surface, (screen_pos[0]-6, screen_pos[1]+1))

    def drawText(self):
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        # render text
        for i, description in enumerate(self.world.descriptions):
            label = self.descriptionFont.render(description[0], False, hex2rgb(description[1]))
            # Magic numbers here, but no need to fix this until we decide to
            # change the scalars in self.getFontRect()
            self.window.blit(label, (10, 350 + 20 * i))
    
    def draw(self, inspecting):
        self.window.fill(self.background_color)
        self.drawViewport()
        self.drawPlayer()
        if inspecting:
            self.drawInspectionCursor()
        self.drawText()

        pygame.display.update()
