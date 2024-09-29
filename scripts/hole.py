import pygame as pg

class Hole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hole_radius = 15
        # Load the image and handle exceptions
        self.image = pg.image.load("data/images/Hole/Hole.png")  # Load image with alpha channel
        self.image = pg.transform.scale(self.image, (self.hole_radius * 2, self.hole_radius * 2))  # Scale image

    def draw(self, screen):
        # Draw the hole image centered at (self.x, self.y)
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)