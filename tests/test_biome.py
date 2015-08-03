
import unittest

from lakeception import biome, lakeutils

class TestBiome(unittest.TestCase):
    def test_main(self):
        files = biome.get_biome_files()
        biomes = {}

        for index, f in enumerate(files):
            print f
            b = biome.Biome(f, index)
            biomes[b.id] = b

        for biomeID in biomes:
            b = biomes[biomeID]
            print "Biome Name:", b.name
            print "Biome ID:", b.id

            print "Tiles:"
            for tile in b.tiles.values():
                print "  <Tile: %s, \"%s\", \"%s\", %s, col=%s, \"%s\">" % (
                    tile.glyph, tile.name, tile.allGlyphs,
                    tile.color, tile.is_collidable, tile.description,
                )

            print "Elevations:"
            for elevation, weightedTiles in sorted(b.elevations.iteritems()):
                print "  %s: %s" % (elevation, weightedTiles)

            print "Pick some random weighted tiles at elevations:"
            import random
            for elevation in xrange(0, 20+1):
                print elevation, b.getTileAtElevation(elevation)
