import random

class World(object):
	def __init__(self, name, dimensions, debug=False):
		self.name = name
		
		if debug:
			self.dimensions = (5, 5) # Force debug world dimensions
			self.tiles = self.generateDebugWorld()
		else:
			self.dimensions = dimensions
			self.tiles = self.generateWorld()
	
	def generateWorld(self):
		waterTile = Tile("water", "some water", "...........,~")
		
		# Flood the world with water!
		# All elements are references to the same water tile to save memory.
		width, height = self.dimensions
		tiles = [waterTile] * (width * height)
		
		return tiles
	
	def generateDebugWorld(self):
		# Use 25 letters of the alphabet for 25 unique tiles.
		# Should help make positional debugging easier:
		#     ABCDE   (0,0)
		#     FGHJI
		#     KLMNO     5x5 world
		#     PQRST
		#     UVWXY          (4,4)
		
		abc = "ABCDEFGHIJKLMNOPQRSTUVWXY"
		tiles = []
		for letter in abc:
			t = Tile(letter, letter, letter+letter.lower())
			tiles.append(t)
		
		return tiles
	
	def _pointToIndex(self, point):
		x, y = point
		width = self.dimensions[0]
		
		index = y * width + x
		
		return index
	
	def _indexToPoint(self, index):
		width = self.dimensions[0]
		
		x = i % width
		y = i // width
		
		return (x, y)
	
	def getTileAtPoint(self, point):
		index = self._pointToIndex(point)
		
		return self.tiles[index]
	
	def getTilesInArea(self, topLeft, bottomRight):
		x1, y1 = topLeft
		x2, y2 = bottomRight
		
		width = x2-x1+1
		height = y2-y1+1
		
		areaTiles = []
		for row in xrange(0, height):
			rowIndex = self._pointToIndex( (x1, y1+row) )
			rowTiles = self.tiles[rowIndex : rowIndex+width]
			areaTiles.extend(rowTiles)
		
		return areaTiles

class Tile(object):
	def __init__(self, name, description, icons):
		self.name = name
		self.description = description
		# A collection of characters representing the tile.
		# A random icon is chosen each frame draw for ~ambience~
		self.icons = icons
	
	def getIcon(self):
		return random.choice(self.icons)
	
	def __str__(self):
		return self.getIcon()
	
	def __repr__(self):
		return self.__str__()

if __name__ == "__main__":
	w = World("Test World", (5,5), debug=True)
	print w.getTilesInArea((0,0), (4,4))
