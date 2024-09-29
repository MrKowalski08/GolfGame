# scripts/tile.py
import pygame as pg

class Tile:
    def __init__(self, x, y, tile_size, tile_type):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.tile_type = tile_type

        # Load tile image based on the type
        self.image = pg.image.load(f"data/images/Walls/{tile_type}.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (tile_size, tile_size))
        
        # Create a rectangle for collision detection
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class TileMap:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.tiles = []

    def load_level(self, level_data):
        self.tiles = []  # Clear existing tiles
        for row_index, row in enumerate(level_data):
            for col_index, tile_type in enumerate(row):
                if tile_type != 0:  # Non-zero means a tile is present
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.tiles.append(Tile(x, y, self.tile_size, tile_type))

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)

    def check_collisions(self, ball):
        for tile in self.tiles:
            if ball.rect.colliderect(tile.rect):
                self.resolve_collision(ball, tile)
