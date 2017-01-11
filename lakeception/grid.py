# -*- coding: utf-8 -*-

import logging

LOGGER = logging.getLogger()


class Grid(object):
    def __init__(self, size, tiles=None, fill=None):
        LOGGER.debug(u'Initializing Grid of size=%s', size)
        
        self.size = None
        self.tiles = None
        
        if not tiles:
            tiles = [fill] * (size[0] * size[1])
        
        self.set_tiles(tiles, size)
    
    def __getitem__(self, key):
        return self.tiles.__getitem__(key)
    
    def __setitem__(self, key, value):
        self.tiles.__setitem__(key, value)
    
    def __delitem__(self, key):
        self.tiles.__delitem__(key)
    
    def __unicode__(self):
        return unicode(self.__str__())
    
    def __str__(self):
        return '<{}.{} object at 0x{:X}, size={}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            id(self),
            self.size
        )
    
    def _point_to_index(self, point):
        x, y = point
        width, height = self.size
        
        return (y % height) * width + (x % width)
    
    def _index_to_point(self, index):
        width = self.size[0]
        
        x = index % width
        y = index // width
        
        return (x, y)
    
    def get_tile_at_point(self, point):
        return self.tiles[self._point_to_index(point)]
    
    def set_tile_at_point(self, point, tile)
        self.tiles[self._point_to_index(point)] = tile
    
    def get_tiles_in_rect(self, top_left, out_grid):
        # Get target area within self
        a, b = top_left
        width, height = out_grid.size
        
        # Fill out_grid with tiles from self
        for y in xrange(b, b+height):
            for x in xrange(a, a+width):
                tile = self.get_tile_at_point((x, y))
                out_grid.set_tile_at_point((x-a, y-b), tile)
    
    def set_tiles_in_rect(self, top_left, in_grid):
        # Get target area within self
        a, b = top_left
        width, height = in_grid.size
        
        # Fill self with tiles from in_grid
        for y in xrange(0, height):
            for x in xrange(0, width):
                tile = in_grid.get_tile_at_point((x, y))
                self.set_tile_at_point((a+x, b+y), tile)
    
    def set_tiles(self, tiles, size):
        width, height = size
        expected_count = width * height
        actual_count = len(tiles)
        
        if expected_count != actual_count:
            raise ValueError(u'Tile count does not match dimensions: {}x{}={} but got {} tiles.'.format(
                width, height, expected_count, actual_count,
            ))
        
        self.size = size
        self.tiles = tiles
