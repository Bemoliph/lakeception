import os

class Screen(object):
	def __init__(self, world):
		self.world = world
	
	def draw(self, topLeft, bottomRight):
		width = bottomRight[0] - topLeft[0] + 1
		height = bottomRight[1] - topLeft[1] + 1
		visibleTiles = self.world.getTilesInArea(topLeft, bottomRight)
		
		
		# TODO:  Is it cheating to use curses?
		os.system('cls' if os.name == 'nt' else 'clear')
		for row in xrange(0, height):
			rowIndex = row*width
			rowIcons = visibleTiles[rowIndex : rowIndex+width]
			print "".join(map(str, rowIcons))
