from world import World
from screen import Screen

class Game(object):
	def __init__(self):
		self.world = World("Test World", (5,5), debug=True)
		self.screen = Screen(self.world)
	
	def tick(self):
		self.screen.draw((1,1), (3,3))

if __name__ == "__main__":
	g = Game()
	g.tick()