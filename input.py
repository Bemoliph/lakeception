# -*- coding: utf-8 -*-
import pygame

class Input(object):
    def __init__(self, game):
        self.game = game
        # Just a shorthand for the player; self.game.world.player is a bit verbose
        self.player = self.game.world.player
        
        repeat_delay    = 250 # ms
        repeat_interval = 500 # ms
        pygame.key.set_repeat(repeat_delay, repeat_interval)
        
        self.key_mapping = {
            pygame.K_UP     : self.moveUp,
            pygame.K_RIGHT  : self.moveRight,
            pygame.K_DOWN   : self.moveDown,
            pygame.K_LEFT   : self.moveLeft,
            pygame.K_ESCAPE : self.quit,
            pygame.K_m   : self.mute,
        }
    
    def handleKey(self, event):
        key = event.key
        
        if key in self.key_mapping:
            self.key_mapping[key]()
    
    def move(self, deltaX, deltaY):
        # Maybe get a direct reference to Player object in Input when there is one?
        currentX, currentY = self.player.pos
        
        newX = currentX + deltaX
        newY = currentY + deltaY
        
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

    def mute(self):
        if not self.game.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.game.muted = not self.game.muted

