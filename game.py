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
        
        self.fps = 60
        self.clock = pygame.time.Clock()
        
        self.ANIMATE = pygame.USEREVENT+0
        self.animation_rate = 1 * 1000
        pygame.time.set_timer(self.ANIMATE, self.animation_rate)
        
        self.updated = True
        self.quitting = False
    
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.input.handleKey(event)
            elif event.type == self.ANIMATE:
                self.screen.draw()
                self.updated = False
            elif event.type == pygame.QUIT:
                self.quitting = True
        
        if self.updated:
            self.screen.draw()
            self.updated = False
        
        timeDelta = self.clock.tick(self.fps)

if __name__ == "__main__":
    g = Game()
    while not g.quitting:
        g.tick()
