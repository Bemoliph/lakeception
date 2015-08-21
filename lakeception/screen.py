# -*- coding: utf-8 -*-
import pygame

from lakeception.lakeutils import hex2rgb, hex2rgba, rgb2hex
from lakeception.tiles import Tile


class Screen(object):
    def __init__(self, world, window_res, viewport_res):
        self.world = world

        self.backgroundColor = hex2rgb("0E0E0E")
        self.window = pygame.display.set_mode(window_res)

        self.viewport_res = viewport_res
        # viewport_res has to be square & odd for viewport_center to be correct
        self.viewport_center = (viewport_res[0] // 2, viewport_res[1] // 2)
        self.viewport_tiles = [None] * (viewport_res[0] * viewport_res[1])

        self.DRAWMODE_NORMAL = 0
        self.DRAWMODE_ELEVATION = 1
        self.DRAWMODE_BIOMES = 2
        self.currentDrawMode = self.DRAWMODE_NORMAL

        self.sprites = {}
        self.font_face = "monospace"
        self.font_size = window_res[0] / self.viewport_res[0]
        self.fonts = {
            (0.5, 0.5): pygame.font.SysFont(self.font_face, self.font_size / 2),  # Half sized font for debug modes
            (1, 1): pygame.font.SysFont(self.font_face, self.font_size),          # Normal sized font for most things
        }
        self.font_dimensions = self.fonts[(1, 1)].size("@")

        self.cursor = (0, 0)
        self.cursor_surface = pygame.Surface((self.font_size, self.font_size), pygame.SRCALPHA, 32)
        self.cursor_surface.fill(hex2rgba("F2F2F2", 50))

        self.descriptionFont = pygame.font.SysFont("monospace", 15)

    def get_font_rect(self, coords):
        # Scalars were experimentally determined so characters touch instead
        # of overlap/gap.  Seems fontDimensions work for big and small font sizes.
        width, height = self.font_dimensions
        height *= 0.85
        width *= 1.75

        x = coords[0] * width
        y = coords[1] * height

        return pygame.Rect((x, y), (width, height))

    def _get_tile_glyph_for_current_draw_mode(self, tile, size):
        if self.currentDrawMode == self.DRAWMODE_NORMAL:
            return unicode(tile.glyph), tile.color, size
        elif self.currentDrawMode == self.DRAWMODE_ELEVATION:
            return unicode(tile.elevation), tile.color, size
        elif self.currentDrawMode == self.DRAWMODE_BIOMES:
            return unicode(tile.biomeID), tile.color, size

    def _generate_glyph_sprite(self, glyph, color, size):
        if self.currentDrawMode != self.DRAWMODE_NORMAL:
            size = (0.5, 0.5)

        if size not in self.fonts:
            self.fonts[size] = pygame.font.SysFont(self.font_face, self.font_size * size[0])

        self.sprites[(glyph, color, size)] = self.fonts[size].render(glyph, False, color, self.backgroundColor)

    def get_sprite(self, tile, coords, size=(1,1)):
        colored_glyph = self._get_tile_glyph_for_current_draw_mode(tile, size)

        if colored_glyph not in self.sprites:
            self._generate_glyph_sprite(*colored_glyph)

        sprite_rect = self.get_font_rect(coords)

        return self.sprites[colored_glyph], sprite_rect

    def draw_viewport(self):
        width, height = self.viewport_res

        self.world.getTilesAroundPlayer((width, height), self.viewport_tiles)

        for y in xrange(0, height):
            for x in xrange(0, width):
                tile = self.viewport_tiles[y * width + x]
                sprite, sprite_rect = self.get_sprite(tile, (x, y))

                self.window.blit(sprite, sprite_rect)

    def draw_player(self):
        player = self.world.ent_man.player
        sprite, sprite_rect = self.get_sprite(player.tile, self.viewport_center, player.size)

        self.window.blit(sprite, sprite_rect)

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
        player_pos = self.world.ent_man.player.pos
        return pos[0] < player_pos[0] - self.viewport_res[0] // 2 or \
            pos[0] > player_pos[0] + self.viewport_res[0] // 2 or \
            pos[1] < player_pos[1] - self.viewport_res[1] // 2 or \
            pos[1] > player_pos[1] + self.viewport_res[1] // 2

    def draw_ais(self):
        ais = self.world.ent_man.ais

        for ai in ais:
            # Cull AIs out of view
            if self.is_out_of_view(ai.pos):
                continue

            # Calculate relative position
            player_pos = self.world.ent_man.player.pos
            rel_pos = (
                ai.pos[0] - player_pos[0] + self.viewport_center[0],
                ai.pos[1] - player_pos[1] + self.viewport_center[1],
            )
            sprite, sprite_rect = self.get_sprite(ai.tile, rel_pos, ai.size)
            self.window.blit(sprite, sprite_rect)

    def draw_inspection_cursor(self, editing):
        player_pos = self.world.ent_man.player.pos
        # world_pos = player position + cursor position
        world_pos = (player_pos[0] + self.cursor[0], player_pos[1] + self.cursor[1])
        # Screen position differs from world position, as we're drawing with
        # respect to the viewport
        screen_pos = (self.viewport_center[0] + self.cursor[0], self.viewport_center[1] + self.cursor[1])
        screen_pos = self.get_font_rect(screen_pos)

        # If the cursor is centered in the viewport => it's hovering above the player
        if self.cursor == (0, 0):
            # Get the player tile
            tile = self.world.ent_man.player.tile
        else:
            potential_entity = self.world.ent_man.get_entity_at_position(world_pos)
            if potential_entity is None:
                tile = self.world.getTileAtPoint(world_pos)
            else:
                tile = potential_entity.tile
        if editing:
            tile_details = u"[EDITING] {0}: {1}, {2}, {3}, #{4}".format(world_pos,
                                                                        tile.glyph, tile.name,
                                                                        tile.getHSV(), rgb2hex(*tile.color))
            self.world.addDescription(tile_details)
        else:
            self.world.addDescription(tile.description)

        # Magic numbers => center the cursor on the tile it's hovering over, kind of
        self.window.blit(self.cursor_surface, (screen_pos[0] - 6, screen_pos[1] + 1))

    def draw_text(self):
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        # render text
        # TODO: add subtle fade over time behaviour to description text
        for i, description in enumerate(self.world.descriptions):
            label = self.descriptionFont.render(description[0], False, hex2rgb(description[1]))
            # Magic numbers here, but no need to fix this until we decide to
            # change the scalars in self.getFontRect()
            self.window.blit(label, (10, 350 + 20 * i))

    def draw(self, inspecting, editing):
        self.window.fill(self.backgroundColor)
        self.draw_viewport()
        self.draw_player()
        self.draw_ais()
        if inspecting:
            self.draw_inspection_cursor(editing)
        self.draw_text()

        pygame.display.update()
