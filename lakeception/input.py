# -*- coding: utf-8 -*-

import pygame


# Enum-like class for keeping track of editor mode
class Editing:
    Hue, Saturation, Brightness, Glyph = range(4)


class Input(object):
    def __init__(self, game):
        self.game = game
        self.bounds = {
            "x": self.game.screen.viewportRes[0] // 2,
            "y": self.game.screen.viewportRes[1] // 2
        }
        # Just a shorthand for the player; self.game.world.player is a bit verbose
        self.player = self.game.world.ent_man.player
        self.hsv = ""
        self.currentEditorMode = Editing.Glyph

        # Both repeat values are in milliseconds
        repeatDelay    = 35 # time between keypress and automatic motion
        repeatInterval = 75 # time between automatic steps
        pygame.key.set_repeat(repeatDelay, repeatInterval)

        self.keyMapping = {
            pygame.K_UP     : self.moveUp,
            pygame.K_RIGHT  : self.moveRight,
            pygame.K_DOWN   : self.moveDown,
            pygame.K_LEFT   : self.moveLeft,
            pygame.K_ESCAPE : self.quit,
            pygame.K_m      : self.mute,
            pygame.K_i      : self.toggleInspection,
            pygame.K_F1     : self.drawNormal,
            pygame.K_F2     : self.drawElevation,
            pygame.K_F3     : self.drawBiomes,
            pygame.K_F4     : self.toggleEditing,
        }

    def handleKey(self, event):
        key = event.key

        # Change editor mode
        if self.game.editing and pygame.key.get_mods() & pygame.KMOD_LCTRL:
            if key == pygame.K_h:
                self.currentEditorMode = Editing.Hue
                print "editing hue"
            elif key == pygame.K_s:
                self.currentEditorMode = Editing.Saturation
                print "editing saturation"
            elif key == pygame.K_b:
                self.currentEditorMode = Editing.Brightness
                print "editing brightness"
            elif key == pygame.K_g:
                self.currentEditorMode = Editing.Glyph
                print "editing glyphs"
        elif key in self.keyMapping:
            self.keyMapping[key]()
        elif self.game.editing:
            self.editTile(event)

    def editTile(self, event):
        tilePos = (self.game.screen.cursor[0] + self.player.pos[0],
                self.game.screen.cursor[1] + self.player.pos[1])
        tile = self.game.world.getTileAtPoint(tilePos)

        if self.currentEditorMode == Editing.Glyph:
            # Set the tile's glyph
            tile.glyph = event.unicode
        else:
            # If we typed a digit, start changing the tile color
            if event.unicode.isdigit():
                self.hsv += event.unicode
                print "adding digit", self.hsv

                # Hue goes all the way up to 360 => self.hsv needs 3 chars
                if len(self.hsv) >= 3 or len(self.hsv) >= 2 and not self.currentEditorMode == Editing.Hue:
                    hsvComponent = int(self.hsv)
                    print hsvComponent
                    if self.currentEditorMode == Editing.Hue:
                        tile.setHue(hsvComponent)
                    elif self.currentEditorMode == Editing.Saturation:
                        tile.setSaturation(hsvComponent)
                    elif self.currentEditorMode == Editing.Brightness:
                        tile.setBrightness(hsvComponent)
                    # Clear hsv string
                    self.hsv = ""
        self.game.updated = True

    def move(self, deltaX, deltaY):
        if self.game.inspecting:
            currentX, currentY = self.game.screen.cursor

            newX = currentX + deltaX
            newY = currentY + deltaY
            if abs(newX) <= self.bounds["x"] and abs(newY) <= self.bounds["y"]:
                self.game.screen.cursor = (newX, newY)
        else:
            self.game.world.move(self.player, (deltaX, deltaY))

            # Small feel/usability tweak:
            # place the cursor in the direction the player was moving
            self.game.screen.cursor = (deltaX, deltaY)

        self.game.updated = True

    def moveUp(self):
        self.move(0, -1)

    def moveRight(self):
        self.move(1, 0)

    def moveDown(self):
        self.move(0, 1)

    def moveLeft(self):
        self.move(-1, 0)

    def quit(self):
        # Exit inspection mode
        if self.game.inspecting:
            self.toggleInspection()
            # Turn off editing
            self.game.editing = False
        # Exit the game
        else:
            self.game.quitting = True

    def toggleInspection(self):
        self.game.inspecting = not self.game.inspecting
        if self.game.editing:
            self.toggleEditing()

        if not self.game.inspecting:
            self.game.screen.cursor = (0, 0)   # reset cursor position
            self.game.world.addDescription("") # clear the message

        self.game.updated = True

    def toggleEditing(self):
        self.game.editing = not self.game.editing
        self.game.inspecting = self.game.editing
        if self.game.editing:
            self.setDrawMode(self.game.screen.DRAWMODE_NORMAL)
            print "cyberterraforming tools online"
        else:
            self.game.world.addDescription("") # clear debug message
            print "cyberterraforming tools offline"
        self.game.updated = True

    def mute(self):
        if not self.game.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        self.game.muted = not self.game.muted

    def setDrawMode(self, mode):
        self.game.screen.currentDrawMode = mode
        self.game.screen.draw(self.game.inspecting, self.game.editing)

    def drawNormal(self):
        self.game.world.addDescription("")
        self.setDrawMode(self.game.screen.DRAWMODE_NORMAL)

    def drawElevation(self):
        self.game.world.addDescription("[DEBUG] Now drawing tile elevations.")
        self.setDrawMode(self.game.screen.DRAWMODE_ELEVATION)

    def drawBiomes(self):
        self.game.world.addDescription("[DEBUG] Now drawing tile biome IDs.")
        self.setDrawMode(self.game.screen.DRAWMODE_BIOMES)
