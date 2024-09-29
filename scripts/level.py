# scripts/level.py
import pygame as pg
from scripts.tile import Tile
from scripts.sounds import *

class Level:
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
                # Calculate the overlap on each side
                overlap_left = ball.rect.right - tile.rect.left
                overlap_right = tile.rect.right - ball.rect.left
                overlap_top = ball.rect.bottom - tile.rect.top
                overlap_bottom = tile.rect.bottom - ball.rect.top
                
                # Find the smallest overlap
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                # Resolve the collision based on the smallest overlap
                if min_overlap == overlap_left:  # Collision on the left
                    ball.x = tile.rect.left - ball.ball_radius
                    ball.velocity[0] = -ball.velocity[0]  # Reverse x velocity
                elif min_overlap == overlap_right:  # Collision on the right
                    ball.x = tile.rect.right + ball.ball_radius
                    ball.velocity[0] = -ball.velocity[0]  # Reverse x velocity
                elif min_overlap == overlap_top:  # Collision on the top
                    ball.y = tile.rect.top - ball.ball_radius
                    ball.velocity[1] = -ball.velocity[1]  # Reverse y velocity
                elif min_overlap == overlap_bottom:  # Collision on the bottom
                    ball.y = tile.rect.bottom + ball.ball_radius
                    ball.velocity[1] = -ball.velocity[1]  # Reverse y velocity
                
                
                # Update the rect's position after repositioning
                ball.rect.topleft = (ball.x - ball.ball_radius, ball.y - ball.ball_radius)
