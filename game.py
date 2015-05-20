from world import World
from screen import Screen
from time import sleep
import pygame
# contains KEYDOWN and other key codes
from pygame.locals import *

class Game(object):
    def __init__(self):
        self.world = World("Test World", (5,5), debug=True)
        self.screen = Screen(self.world, 800, 400)
   
    def tick(self):
        self.screen.draw((0,0), (12,12))


if __name__ == "__main__":
    g = Game()
    stillWannaPlay = True
    while stillWannaPlay:
        g.tick()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                key = event.key
                # INPUT TOWN
                if key == K_UP:
                    move(0, -1)
                elif key == K_RIGHT:
                    move(1, 0)
                elif key == K_DOWN:
                    move(0, 1)
                elif key == K_LEFT:
                    move(-1, 0)
            # player quits q.q
            elif event.type == QUIT:
                stillWannaPlay = False
                break
        pygame.display.update()


