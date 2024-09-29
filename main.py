# main.py
import pygame as pg
import math
import sys
from scripts.ball import Ball
from scripts.hole import Hole
from scripts.level import Level
from scripts.levels import *

def calculate_dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

class MainMenu:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((640, 512))  # Screen size
        pg.display.set_caption("Game Title")
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 74)  # Title font
        self.button_font = pg.font.Font(None, 48)  # Button font
        self.running = True

    def draw_title(self):
        title_text = pg.image.load("data/images/Golf.png")
        title_rect = title_text.get_rect(center=(320, 200))
        self.screen.blit(title_text, title_rect)

    def draw_button(self):
        button_text = self.button_font.render("Start Game", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(320, 300))
        button_background = pg.Surface(button_rect.size)
        button_background.fill((0, 0, 0))  # Black background for the button
        button_background.set_alpha(128)  # Set transparency
        self.screen.blit(button_background, button_rect.topleft)  # Draw button background
        self.screen.blit(button_text, button_rect.topleft)

        return button_rect

    def run(self):
        while self.running:
            self.background = pg.image.load("data/images/Ground/1.png").convert()
            self.background = pg.transform.scale(self.background, (640, 512))
            self.screen.blit(self.background, (0, 0))
            self.draw_title()
            button_rect = self.draw_button()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(pg.mouse.get_pos()):
                        print("Start Game Clicked!")
                        return  # Exit main menu to start the game

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()
        sys.exit()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((640, 512))
        self.clock = pg.time.Clock()
        pg.display.set_caption("Game with Multiple Levels")

        # Load background image
        self.background = pg.image.load("data/images/Ground/1.png").convert()
        self.background = pg.transform.scale(self.background, (640, 512))

        # Levels
        self.current_level = 0
        self.levels = levels

        # Initialize level, ball, and hole
        self.level = Level(64)
        self.level.load_level(self.levels[self.current_level])
        self.ball = Ball(80, 80)
        self.hole = Hole(544, 416)  # Adjust hole position as per level design
        
        # Movement counter
        self.move_counter = 0  # Initialize movement counter

    def run(self):
        dragging = False
        while True:
            # Draw background
            self.screen.blit(self.background, (0, 0))

            # Draw level, ball, and hole
            self.level.draw(self.screen)
            self.ball.draw(self.screen)
            self.hole.draw(self.screen)

            # Display the movement counter
            move_counter_text = pg.font.Font(None, 36).render(f'Moves: {self.move_counter}', True, (255, 255, 255))
            self.screen.blit(move_counter_text, (10, 10))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                # Mouse button down to start dragging ball
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    if calculate_dist(mouse_x, mouse_y, self.ball.x, self.ball.y) <= self.ball.ball_radius:
                        dragging = True

                # Mouse button up to release the ball and apply velocity
                if event.type == pg.MOUSEBUTTONUP and dragging:
                    dragging = False
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    dx = mouse_x - self.ball.x
                    dy = mouse_y - self.ball.y
                    distance = calculate_dist(mouse_x, mouse_y, self.ball.x, self.ball.y)
                    angle = math.atan2(dy, dx)

                    # Apply velocity in the opposite direction of the drag
                    power = min(distance, 100)
                    self.ball.velocity[0] = -math.cos(angle) * power * 0.1
                    self.ball.velocity[1] = -math.sin(angle) * power * 0.1

                    # Increment move counter
                    self.move_counter += 1  # Increment on each move

            # Draw line between ball and mouse
            if dragging:
                m_x, m_y = pg.mouse.get_pos()
                pg.draw.line(self.screen, (0, 0, 0), (self.ball.x, self.ball.y), (m_x, m_y), 2)

            # Move the ball
            self.ball.move()

            # Check for collisions with tiles
            self.level.check_collisions(self.ball)

            # Check if ball is in the hole
            if self.check_ball_in_hole():
                self.fade_transition()
                self.next_level()

            pg.display.flip()
            self.clock.tick(60)

    def check_ball_in_hole(self):
        return calculate_dist(self.ball.x, self.ball.y, self.hole.x, self.hole.y) < (self.hole.hole_radius + self.ball.ball_radius)

    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.levels):
            self.level.load_level(self.levels[self.current_level])
            self.ball.x, self.ball.y = 80, 80
            self.ball.velocity = [0, 0]
        else:
            print("You completed all levels!")
            pg.quit()
            sys.exit()

    def fade_transition(self, duration=500):
        fade_surface = pg.Surface((640, 512))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 255):
            fade_surface.set_alpha(alpha)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(fade_surface, (0, 0))
            pg.display.flip()
            pg.time.delay(duration // 255)  # Control speed of the fade

# Run the main menu first
def main():
    menu = MainMenu()
    menu.run()
    
    # After the menu, run the game
    game = Game()
    
    # Start transition to the game
    game.fade_transition()
    game.run()

main()
