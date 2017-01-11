# -*- coding: utf-8 -*-

import unittest

from lakeception.grid import Grid


class TestGrid(unittest.TestCase):
    def setUp(self):
        # Use cool pipe shapes to make positional debugging easier:
        #     ╔═══╗   (0,0)
        #     ║123║
        #     ║456║    5x5 world
        #     ║789║
        #     ╚═══╝          (4,4)
        self.pipe_layout = u'╔═══╗║123║║456║║789║╚═══╝'
        self.pipe_tiles = list(self.pipe_layout)
        self.pipe_size = (5, 5)
    
    def test_empty_grid(self):
        width = 5
        height = 7
        fill_tile = None
        g = Grid(size=(width, height), fill=fill_tile)
        
        self.assertTrue(
            all(x == fill_tile for x in g.tiles),
            u'g should be empty, but at least one element is not.'
        )
    
    def test_filled_grid(self):
        width = 5
        height = 7
        fill_tile = u'x'
        g = Grid(size=(width, height), fill=fill_tile)
        
        self.assertTrue(
            all(x == fill_tile for x in g.tiles),
            u'g should be filled with {}, but at least one element is not.'.format(
                fill_tile
            )
        )
    
    def test_size_versus_count(self):
        width = 5
        height = 7
        g = Grid(size=(width, height))
        
        expected_count = width * height
        actual_count = len(g.tiles)
        
        self.assertEqual(
            expected_count, actual_count,
            u'Tile count should be {} based on dimensions, but is {}'.format(
                expected_count, actual_count,
            )
        )
    
    def test_set_tiles_contents(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        self.assertEqual(
            g.tiles, self.pipe_tiles,
            u'Tile contents didn\'t match input contents.'
        )
    
    def test_set_tiles_size(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        self.assertEqual(
            g.size, self.pipe_size,
            u'Grid size didn\'t match input size.'
        )
    
    def test_get_tile_at_point(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        point = (1, 3)
        expected_tile = u'7'
        actual_tile = g.get_tile_at_point(point)
        
        self.assertEqual(
            expected_tile, actual_tile,
            u'Tile {} should have been {}, found {}'.format(
                point, expected_tile, actual_tile
            )
        )
    
    def test_get_tile_at_point_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        point = (8, 7)
        expected_tile = u'6'
        actual_tile = g.get_tile_at_point(point)
        
        self.assertEqual(
            expected_tile, actual_tile,
            u'Tile {} should have been {}, found {}'.format(
                point, expected_tile, actual_tile
            )
        )
    
    def test_point_to_index(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        point = (3, 1) # u'3'
        expected_index = 8
        actual_index = g._point_to_index(point)
        
        self.assertEqual(
            expected_index, actual_index,
            u'Index of {} should have been {}, found {}'.format(
                point, expected_index, actual_index
            )
        )
    
    def test_point_to_index_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        point = (11, 12) # u'4'
        expected_index = 11
        actual_index = g._point_to_index(point)
        
        self.assertEqual(
            expected_index, actual_index,
            u'Index of {} should have been {}, found {}'.format(
                point, expected_index, actual_index
            )
        )
    
    def test_point_to_index_negative(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        point = (-2, -3) # u'6'
        expected_index = 13
        actual_index = g._point_to_index(point)
        
        self.assertEqual(
            expected_index, actual_index,
            u'Index of {} should have been {}, found {}'.format(
                point, expected_index, actual_index
            )
        )
    
    def test_point_to_index_negative_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        point = (-12, -2) # u'9'
        expected_index = 18
        actual_index = g._point_to_index(point)
        
        self.assertEqual(
            expected_index, actual_index,
            u'Index of {} should have been {}, found {}'.format(
                point, expected_index, actual_index
            )
        )
    
    def test_index_to_point(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        index = 17 # u'8'
        expected_point = (2, 3)
        actual_point = g._index_to_point(index)
        
        self.assertEqual(
            expected_point, actual_point,
            u'Index {} should have produced point {}, found {}'.format(
                index, expected_point, actual_point
            )
        )
    
    def test_index_to_point_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        index = 32 # u'2'
        expected_point = (2, 1)
        actual_point = g._index_to_point(index)
        
        self.assertEqual(
            expected_point, actual_point,
            u'Index {} should have produced point {}, found {}'.format(
                index, expected_point, actual_point
            )
        )
        
    def test_index_to_point_negative(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        index = -8 # u'8'
        expected_point = (2, 3)
        actual_point = g._index_to_point(index)
        
        self.assertEqual(
            expected_point, actual_point,
            u'Index {} should have produced point {}, found {}'.format(
                index, expected_point, actual_point
            )
        )
        
    def test_index_to_point_negative_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        index = -67 # u'3'
        expected_point = (3, 1)
        actual_point = g._index_to_point(index)
        
        self.assertEqual(
            expected_point, actual_point,
            u'Index {} should have produced point {}, found {}'.format(
                index, expected_point, actual_point
            )
        )
    
    def test_set_tile_at_point(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        expected_tile = u'x'
        point = (1, 2) # u'4'
        index = 11
        
        g.set_tile_at_point(point, expected_tile)
        actual_tile = g[index]
        
        self.assertEqual(
            expected_tile, actual_tile,
            u'Tile at {} ({}) should have been {}, found {}'.format(
                point, index, expected_tile, actual_tile
            )
        )
    
    def test_set_tile_at_point_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        expected_tile = u'x'
        point = (13, 7) # u'6'
        index = 13
        
        g.set_tile_at_point(point, expected_tile)
        actual_tile = g[index]
        
        self.assertEqual(
            expected_tile, actual_tile,
            u'Tile at {} ({}) should have been {}, found {}'.format(
                point, index, expected_tile, actual_tile
            )
        )
    
    def test_get_tiles_in_rect(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        x = Grid(size=(3, 3))
        top_left = (1, 1)
        
        g.get_tiles_in_rect(top_left, x)
        
        expected_tiles = list(u'123456789')
        actual_tiles = x.tiles
        
        self.assertEqual(
            expected_tiles, actual_tiles,
            u'Grid x should have contained {}, found {}'.format(
                expected_tiles, actual_tiles
            )
        )
    
    def test_get_tiles_in_rect_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        x = Grid(size=(3, 3))
        top_left = (3, 3)
        
        g.get_tiles_in_rect(top_left, x)
        
        expected_tiles = list(u'9║║═╝╚═╗╔')
        actual_tiles = x.tiles
        
        self.assertEqual(
            expected_tiles, actual_tiles,
            u'Grid x should have contained {}, found {}'.format(
                expected_tiles, actual_tiles
            )
        )
    
    def test_set_tiles_in_rect(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        x = Grid(size=(3, 3), fill=u'x')
        top_left = (1, 1)
        
        g.set_tiles_in_rect(top_left, x)
        
        expected_tiles = list(u'╔═══╗║xxx║║xxx║║xxx║╚═══╝')
        actual_tiles = g.tiles
        
        self.assertEqual(
            expected_tiles, actual_tiles,
            u'Grid g should have contained {}, found {}'.format(
                expected_tiles, actual_tiles
            )
        )
    
    def test_set_tiles_in_rect_wrap(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        x = Grid(size=(3, 3), fill=u'x')
        top_left = (3, 3)
        
        g.set_tiles_in_rect(top_left, x)
        
        expected_tiles = list(u'x══xx║123║║456║x78xxx══xx')
        actual_tiles = g.tiles
        
        self.assertEqual(
            expected_tiles, actual_tiles,
            u'Grid g should have contained {}, found {}'.format(
                expected_tiles, actual_tiles
            )
        )
    
    def test_is_equivalent_point(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        p1 = (-8, -2) # u'8'
        p2 = ( 2,  3) # u'8'
        
        self.assertTrue(
            g.is_equivalent_point(p1, p2),
            u'{} and {} are not equivalent, but both map to u\'8\''.format(
                p1, p2
            )
        )
    
    def test_is_not_equivalent_point(self):
        g = Grid(size=self.pipe_size, tiles=self.pipe_tiles)
        
        p1 = (-8, -2) # u'8'
        p2 = ( 1,  3) # u'7'
        
        self.assertFalse(
            g.is_equivalent_point(p1, p2),
            u'{} and {} are equivalent, but they map to u\'8\' and u\'7\''.format(
                p1, p2
            )
        )
