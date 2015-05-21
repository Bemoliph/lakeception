# -*- coding: utf-8 -*-
import pygame

from world import World
from screen import Screen
from input import Input

class Game(object):
    def __init__(self):
        pygame.init()
        
        self.world = World("Test World", (5,5), debug=True)
        self.screen = Screen(self.world, (300, 300), (10, 10))
        self.input = Input(self)
        
        self.framerate = 60
        self.clock = pygame.time.Clock()
        
        self.quitting = False
    
    def tick(self):
        self.input.tick()
        self.screen.draw()
        self.clock.tick(self.framerate)

if __name__ == "__main__":
    g = Game()
    while not g.quitting:
        g.tick()
