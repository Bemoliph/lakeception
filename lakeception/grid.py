# -*- coding: utf-8 -*-

import logging

LOGGER = logging.getLogger()


class Grid(object):
    u"""A rectangular grid that can store any mixture of types.  Supports coordinate-based access."""
    def __init__(self, size, items=None):
        LOGGER.debug(u'Initializing Grid of size=%s', size)
        
        self.size = None
        self.items = None
        
        if items:
            self.set_items(items, size)
        else:
            self.set_size(size)
    
    def __getitem__(self, key):
        return self.items.__getitem__(key)
    
    def __setitem__(self, key, value):
        self.items.__setitem__(key, value)
    
    def __delitem__(self, key):
        self.items.__delitem__(key)
    
    def __unicode__(self):
        return unicode(self.__str__())
    
    def __str__(self):
        return u'<{}.{} object at 0x{:X}, size={}>'.format(
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
        y = index // width % 5
        
        return x, y
    
    def is_equivalent_point(self, p1, p2):
        u"""
        Determines if two points are equivalent in terms of a wrapping coordinate system.

        :param p1: (x, y) coordinate
        :param p2: (x, y) coordinate
        :return: True if both points refer to the same location.  False if they are distinct locations.
        """
        i1 = self._point_to_index(p1)
        i2 = self._point_to_index(p2)
        
        return i1 == i2
    
    def get_item_at_point(self, point):
        u"""
        Retrieves the object stored at the given point.

        :param point: (x, y) coordinate within the grid.
        :return: The object stored at the given point.
        """
        return self.items[self._point_to_index(point)]
    
    def set_item_at_point(self, point, item):
        u"""
        Stores the object at the given coordinate.

        :param point: (x, y) coordinate within the grid.
        :param item: The object to be stored at the given point.
        """
        self.items[self._point_to_index(point)] = item
    
    def get_items_in_area(self, top_left, out_grid):
        u"""
        Fills another grid with the contents of this grid, based on target grid's size and starting from top_left.

        :param top_left: Point in this grid to start copying from.  Starts at top left and ends at bottom right.
        :param out_grid: Grid object to copy to.
        """
        # Get target area within self
        a, b = top_left
        width, height = out_grid.size
        
        # Fill out_grid with items from self
        for y in xrange(b, b + height):
            for x in xrange(a, a + width):
                item = self.get_item_at_point((x, y))
                out_grid.set_item_at_point((x - a, y - b), item)
    
    def set_items_from_grid(self, top_left, in_grid):
        u"""
        Copies the contents of another grid to this grid, pasting it starting at top_left.

        :param top_left: Point in this grid to start pasting at.  Starts at top left and ends at bottom right.
        :param in_grid: Grid object to copy from.
        """
        # Get target area within self
        a, b = top_left
        width, height = in_grid.size
        
        # Fill self with items from in_grid
        for y in xrange(0, height):
            for x in xrange(0, width):
                item = in_grid.get_item_at_point((x, y))
                self.set_item_at_point((a + x, b + y), item)
    
    def is_valid_size(self, size):
        if not all(type(x) == int for x in size):
            raise TypeError(u'Grid dimensions must be of type int, gave ({}, {})'.format(*map(type, size)))
        else:
            return True
    
    def set_size(self, size):
        u"""
        Resizes the grid, filling it with None.  Does nothing if no change in size.

        :param size: New dimensions of the grid.
        :return: Whether or not the grid actually was resized.
        """
        if self.size != size and self.is_valid_size(size):
            items = [None] * (size[0] * size[1])
            self.set_items(items, size)

            return True
        else:
            return False
    
    def set_items(self, items, size):
        u"""
        Replaces the grid's items with the given items.

        :param items: Iterable of new items to use within the grid.
        :param size: New dimensions of the grid.  Area must match item count.
        """
        if self.is_valid_size(size):
            width, height = size
            expected_count = width * height
            actual_count = len(items)
            
            if expected_count != actual_count:
                raise ValueError(u'Item count does not match dimensions: {}x{}={} but got {} items.'.format(
                    width, height, expected_count, actual_count,
                ))
            
            self.size = size
            self.items = items
