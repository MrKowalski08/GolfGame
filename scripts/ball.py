# scripts/ball.py
import pygame as pg

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]  # Initialize with zero velocity
        self.ball_radius = 10  # Radius of the ball
        self.image = pg.image.load("data/images/Ball/Ball.png")
        self.image = pg.transform.scale(self.image, (self.ball_radius * 2, self.ball_radius * 2))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def move(self):
        screen_width = 640  # Define the screen width
        screen_height = 512  # Define the screen height
        
        # Update the ball's position based on its velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]

                # Apply friction to slow down the ball
        self.velocity[0] *= 0.99
        self.velocity[1] *= 0.99

        # Stop the ball if the velocity is very small
        if abs(self.velocity[0]) < 0.1:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < 0.1:
            self.velocity[1] = 0
