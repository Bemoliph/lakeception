# -*- coding: utf-8 -*-
import pygame

from lakeception.lakeutils import hex2rgb, hex2rgba, rgb2hex
from lakeception.tiles import Tile


class Screen(object):
    def __init__(self, world, windowRes, viewportRes):
        self.world = world

        self.backgroundColor = hex2rgb("0E0E0E")
        self.window = pygame.display.set_mode(windowRes)

        self.viewportRes = viewportRes
        # viewportRes has to be square & odd for viewportCenter to be correct
        self.viewportCenter = (viewportRes[0] // 2, viewportRes[1] // 2)
        self.viewportTiles = [None] * (viewportRes[0] * viewportRes[1])

        self.DRAWMODE_NORMAL = 0
        self.DRAWMODE_ELEVATION = 1
        self.DRAWMODE_BIOMES = 2
        self.currentDrawMode = self.DRAWMODE_NORMAL

        self.sprites = {}
        self.fontFace = "monospace"
        self.fontSize = windowRes[0] / self.viewportRes[0]
        self.font = pygame.font.SysFont(self.fontFace, self.fontSize)
        self.fontMini = pygame.font.SysFont(self.fontFace, self.fontSize/2)
        self.fontDimensions = self.font.size("@")

        self.cursor = (0, 0)
        self.cursorSurface = pygame.Surface((self.fontSize, self.fontSize), pygame.SRCALPHA, 32)
        self.cursorSurface.fill(hex2rgba("F2F2F2", 50))

        self.descriptionFont = pygame.font.SysFont("monospace", 15)

    def getFontRect(self, coords, text):
        # Scalars were experimentally determined so characters touch instead
        # of overlap/gap.  Seems fontDimensions work for big and small font sizes.
        width, height = self.fontDimensions
        height *= 0.85
        width *= 1.75

        x = coords[0] * width
        y = coords[1] * height

        return pygame.Rect((x, y), (width, height))

    def _getTileGlyphForCurrentDrawMode(self, tile):
        if self.currentDrawMode == self.DRAWMODE_NORMAL:
            return (unicode(tile.glyph), tile.color)
        elif self.currentDrawMode == self.DRAWMODE_ELEVATION:
            return (unicode(tile.elevation), tile.color)
        elif self.currentDrawMode == self.DRAWMODE_BIOMES:
            return (unicode(tile.biomeID), tile.color)

    def _generateGlyphSprite(self, glyph, color):
        if self.currentDrawMode == self.DRAWMODE_NORMAL:
            self.sprites[(glyph, color)] = self.font.render(glyph, False, color, self.backgroundColor)
        else:
            self.sprites[(glyph, color)] = self.fontMini.render(glyph, False, color, self.backgroundColor)

    def getSprite(self, tile, coords):
        coloredGlyph = self._getTileGlyphForCurrentDrawMode(tile)

        if coloredGlyph not in self.sprites:
            self._generateGlyphSprite(*coloredGlyph)

        spriteRect = self.getFontRect(coords, coloredGlyph[0])

        return self.sprites[coloredGlyph], spriteRect

    def drawViewport(self):
        width, height = self.viewportRes

        self.world.getTilesAroundPlayer((width, height), self.viewportTiles)

        for y in xrange(0, height):
            for x in xrange(0, width):
                tile = self.viewportTiles[y * width + x]
                sprite, spriteRect = self.getSprite(tile, (x,y))

                self.window.blit(sprite, spriteRect)

    def drawPlayer(self):
        player = self.world.ent_man.player
        sprite, spriteRect = self.getSprite(player.tile, self.viewportCenter)

        self.window.blit(sprite, spriteRect)


    def is_out_of_view(self, pos):
        """
        Checks if a position is out of view of the window, for culling far away
        entities.

        Parameters
        ----------
        pos : tuple of int, int

        Returns
        -------
        bool
        """
        playerPos = self.world.ent_man.player.pos
        return pos[0] < playerPos[0] - self.viewportRes[0] // 2 or \
            pos[0] > playerPos[0] + self.viewportRes[0] // 2 or \
            pos[1] < playerPos[1] - self.viewportRes[1] // 2 or \
            pos[1] > playerPos[1] + self.viewportRes[1] // 2


    def draw_ais(self):
        ais = self.world.ent_man.ais

        for ai in ais:
            # Cull AIs out of view
            if self.is_out_of_view(ai.pos):
                continue

            # Calculate relative position
            playerPos = self.world.ent_man.player.pos
            rel_pos = (
                ai.pos[0] - playerPos[0] + self.viewportCenter[0],
                ai.pos[1] - playerPos[1] + self.viewportCenter[1],
            )
            sprite, spriteRect = self.getSprite(ai.tile, rel_pos)
            self.window.blit(sprite, spriteRect)


    def drawInspectionCursor(self, editing):
        playerPos = self.world.ent_man.player.pos
        # worldPos = player position + cursor position
        worldPos = (playerPos[0] + self.cursor[0], playerPos[1] + self.cursor[1])
        # Screen position differs from world position, as we're drawing with
        # respect to the viewport
        screenPos = (self.viewportCenter[0] + self.cursor[0], self.viewportCenter[1] + self.cursor[1])
        screenPos = self.getFontRect(screenPos, "#")

        # If the cursor is centered in the viewport => it's hovering above the player
        if self.cursor == (0, 0):
            # Get the player tile
            tile = self.world.ent_man.player.tile
        else:
            potentialEntity = self.world.ent_man.get_entity_at_position(worldPos)
            if potentialEntity == None:
                tile = self.world.getTileAtPoint(worldPos)
            else:
                tile = potentialEntity.tile
        if editing:
            text = "[EDITING] {0}, {1}, {2}, #{3}".format(tile.glyph, tile.name,
                    tile.getHSV(), rgb2hex(*tile.color))
            self.world.addDescription(text)
        else:
            self.world.addDescription(tile.description)

        # Magic numbers => center the cursor on the tile it's hovering over, kind of
        self.window.blit(self.cursorSurface, (screenPos[0]-6, screenPos[1]+1))

    def drawText(self):
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        # render text
        for i, description in enumerate(self.world.descriptions):
            label = self.descriptionFont.render(description[0], False, hex2rgb(description[1]))
            # Magic numbers here, but no need to fix this until we decide to
            # change the scalars in self.getFontRect()
            self.window.blit(label, (10, 350 + 20 * i))

    def draw(self, inspecting, editing):
        self.window.fill(self.backgroundColor)
        self.drawViewport()
        self.drawPlayer()
        self.draw_ais()
        if inspecting:
            self.drawInspectionCursor(editing)
        self.drawText()

        pygame.display.update()
