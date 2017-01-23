# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import json
import logging
import noise
import os

from lakeception.lakeutils import get_abs_asset_path, get_weighted_random_choice
from lakeception.tile import TileFactory

LOGGER = logging.getLogger()


class Biome(object):
    BIOMES_DIR = u'biomes'

    def __init__(self, biome_path):
        self.biome_path = get_abs_asset_path(biome_path)

        # These are populated by load(), but listed here for clarity.
        self.name = u''
        self.id = 0
        self.tiles = {}
        self.elevations = {}

        self.load()

    def get_tile(self, elevation):
        # Choose a random tile type assigned to this elevation based on occurrence weight
        elevation = str(elevation)
        weighted_tiles = self.elevations.get(elevation, self.elevations[u'default'])
        choice_index = get_weighted_random_choice([x[1] for x in weighted_tiles])
        tile_name = weighted_tiles[choice_index][0]

        # Get tile definition
        tile_data = self.tiles[tile_name]

        return TileFactory.get_tile(
            tile_data[u'glyph'],
            tile_data[u'color'],
            tile_data[u'desc'],
            tile_data[u'is_collidable'],
        )

    def load(self):
        # Load data directly into Biome object as attributes
        # This lets us access it like b.name, b.tiles, etc.
        with open(self.biome_path, u'r') as biome_file:
            for k, v in json.load(biome_file).iteritems():
                setattr(self, k, v)

    def save(self):
        with open(self.biome_path, u'w') as biome_file:
            json.dump({
                u'name': self.name,
                u'id': self.id,
                u'tiles': self.tiles,
                u'elevations': self.elevations,
            }, biome_file)


class NoiseTerrain(object):
    def __init__(self, dimensions):
        self.dimensions = dimensions

        # Lower frequency -> blurrier blotches
        self.biome_frequency = 0.009
        self.elevation_frequency = 0.025

        self.biomes = self.load_biomes()

    def load_biomes(self):
        biomes_dir = get_abs_asset_path(Biome.BIOMES_DIR)

        biomes = {}
        for biome_path in os.listdir(biomes_dir):
            if biome_path.endswith(u'.biome'):
                b = Biome(os.path.join(biomes_dir, biome_path))
                biomes[b.id] = b

        return biomes

    def get_biome_at(self, point):
        x, y, width, height = (
            e * self.biome_frequency
            for e in point + self.dimensions
        )

        noise_value = noise.snoise2(
            x, y,
            repeatx=width, repeaty=height
        )

        # Convert to biome ID
        biome_count = len(self.biomes)
        biome_id = int(round((noise_value + 1) * (biome_count - 1) / 2))

        return self.biomes.get(biome_id)

    def get_elevation_at(self, point):
        x, y, width, height = (
            e * self.elevation_frequency
            for e in point + self.dimensions
        )

        noise_value = noise.snoise2(
            x, y,
            octaves=10,
            repeatx=width, repeaty=height
        )

        # Constrain elevations to [0, 20]
        elevation = int(round((noise_value + 1) * 10))

        return elevation

    def get_tile_at(self, point):
        biome = self.get_biome_at(point)
        elevation = self.get_elevation_at(point)

        return biome.get_tile(elevation)

    def generate_area(self):
        width, height = self.dimensions

        tiles = [
            self.get_tile_at((x, y))
            for x in xrange(0, width)
            for y in xrange(0, height)
        ]

        return tiles, self.dimensions
