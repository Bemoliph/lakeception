from world import World
from screen import Screen
from time import sleep

class Game(object):
	def __init__(self):
		self.world = World("Test World", (5,5), debug=True)
		self.screen = Screen(self.world)
	
	def tick(self):
		self.screen.draw((0,0), (12,12))

if __name__ == "__main__":
	g = Game()
	g.tick()
