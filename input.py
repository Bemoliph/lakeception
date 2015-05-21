# -*- coding: utf-8 -*-
import pygame

class Input(object):
    def __init__(self, game):
        self.game = game
        
        self.keyMapping = {
            pygame.K_UP     : self.moveUp,
            pygame.K_RIGHT  : self.moveRight,
            pygame.K_DOWN   : self.moveDown,
            pygame.K_LEFT   : self.moveLeft,
            pygame.K_ESCAPE : self.quit,
        }
    
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
                
                if key in self.keyMapping:
                    self.keyMapping[key]()
            elif event.type == pygame.QUIT:
                self.game.quitting = True
    
    def move(self, deltaX, deltaY):
        # Maybe get a direct reference to Player object in Input when there is one?
        currentX, currentY = self.game.world.player_pos
        
        newX = currentX + deltaX
        newY = currentY + deltaY
        
        self.game.world.player_pos = (newX, newY)
    
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