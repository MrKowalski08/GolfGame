import pygame as pg

from scripts.tile import Tile

class TileMap:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.tiles = []

    def load_level(self, tilemap):
        self.tiles = []
        for row_index, row in enumerate(tilemap):
            for col_index, tile_type in enumerate(row):
                if tile_type != 0:  # 0 represents an empty tile
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    tile = Tile(x, y, tile_type, self.tile_size)
                    self.tiles.append(tile)

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)
