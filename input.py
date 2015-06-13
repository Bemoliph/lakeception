# -*- coding: utf-8 -*-
import pygame

class Input(object):
    def __init__(self, game):
        self.game = game
        self.bounds = {
                "x": self.game.screen.viewportRes[0] // 2,
                "y": self.game.screen.viewportRes[1] // 2
            }
        # Just a shorthand for the player; self.game.world.player is a bit verbose
        self.player = self.game.world.player
        
        # Both repeat values are in milliseconds
        repeatDelay    = 35 # time between keypress and automatic motion
        repeatInterval = 175 # time between automatic steps 
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
        }
    
    def handleKey(self, event):
        key = event.key
        
        if key in self.keyMapping:
            self.keyMapping[key]()
    
    def move(self, deltaX, deltaY):
        if self.game.inspecting:
            currentX, currentY = self.game.screen.cursor

            newX = currentX + deltaX
            newY = currentY + deltaY
            if abs(newX) <= self.bounds["x"] and abs(newY) <= self.bounds["y"]:
                self.game.screen.cursor = (newX, newY)
        else:
            currentX, currentY = self.player.pos

            newX = currentX + deltaX
            newY = currentY + deltaY
            # Small feel/usability tweak: 
            # place the cursor in the direction the player was moving
            self.game.screen.cursor = (deltaX, deltaY)

            tile = self.game.world.getTileAtPoint((newX, newY))
            if not tile.collidable:
                self.player.pos = (newX, newY)
        
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
        self.game.quitting = True

    def toggleInspection(self):
        self.game.inspecting = not self.game.inspecting
        
        if not self.game.inspecting:
            self.game.screen.cursor = (0, 0)   # reset cursor position
            self.game.world.addDescription("") # clear the message
        
        self.game.updated = True

    def mute(self):
        if not self.game.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        
        self.game.muted = not self.game.muted
    
    def setDrawMode(self, mode):
        self.game.screen.currentDrawMode = mode
        self.game.screen.draw(self.game.inspecting)
    
    def drawNormal(self):
        self.game.world.addDescription("")
        self.setDrawMode(self.game.screen.DRAWMODE_NORMAL)
    
    def drawElevation(self):
        self.game.world.addDescription("[DEBUG] Now drawing tile elevations.")
        self.setDrawMode(self.game.screen.DRAWMODE_ELEVATION)
    
    def drawBiomes(self):
        self.game.world.addDescription("[DEBUG] Now drawing tile biome IDs.")
        self.setDrawMode(self.game.screen.DRAWMODE_BIOMES)
