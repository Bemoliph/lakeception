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
		worldWidth, worldHeight = self.dimensions
		tiles = [waterTile] * (worldWidth * worldHeight)
		
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
		worldWidth = self.dimensions[0]
		
		index = y * worldWidth + x
		
		return index
	
	def _indexToPoint(self, index):
		worldWidth = self.dimensions[0]
		
		x = i % worldWidth
		y = i // worldWidth
		
		return (x, y)
	
	def getTileAtPoint(self, point):
		index = self._pointToIndex(point)
		
		return self.tiles[index]
	
	def getTilesInArea(self, topLeft, bottomRight):
		worldWidth = self.dimensions[0]
		
		x1, y1 = topLeft
		x2, y2 = bottomRight
		
		areaWidth = x2-x1+1
		areaHeight = y2-y1+1
		
		areaTiles = []
		for row in xrange(0, areaHeight):
			# Add "actual" tiles to row
			row = row % self.dimensions[1] # vertically wrap if row out of bounds
			rowStart = self._pointToIndex( (x1, y1+row) )
			rowEnd = (row + 1) * worldWidth
			rowTiles = self.tiles[rowStart : rowEnd]
			
			# Add horizontal repeats as necessary to support visual world looping
			# Actual + Full Width Repeats + Tail End Repeat
			# [3 4 5]+[1 2 3 4 5][1 2 3 4 5]+[1 2 3]
			repeatWidth = areaWidth - len(rowTiles)
			if repeatWidth:
				# Add any full width repeats
				repeatCount = repeatWidth // worldWidth
				repeatStart = row * worldWidth
				rowTiles.extend(self.tiles[repeatStart : repeatStart+worldWidth] * repeatCount)
				
				# Add any "tail end" repeat
				tailWidth = repeatWidth % worldWidth
				rowTiles.extend(self.tiles[repeatStart : repeatStart+tailWidth])
			
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
	print w.getTilesInArea((0,0), (4,3))
