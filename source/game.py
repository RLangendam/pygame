from source.level import Level
from source.player import Player
from source.constants import Constants
from source.camera import Camera


import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.constants = Constants()  # Initialize constants
        self.screen = pygame.display.set_mode(
            self.constants.screen_dimensions
        )  # Set the screen size
        pygame.display.set_caption("KeiTV game")

        self.clock = pygame.time.Clock()

        self.level_group = pygame.sprite.Group()  # Create a group for level tiles
        self.level = Level(
            self.level_group, self.constants
        )  # Create a level with specified dimensions

        self.player = Player(
            50, 50, self.constants, self.level
        )  # Create a player at position (50, 50)
        self.player_group = pygame.sprite.GroupSingle(self.player)  # type: ignore

        self.camera = Camera(
            self.constants, self.level, self.player
        )  # Create a camera for the game

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(
                self.constants.fps
            )  # Get the time since the last frame in milliseconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update player
            self.player_group.update(dt)
            self.camera.update()

            self.camera.draw(
                self.screen, self.level_group, self.player_group
            )  # Draw camera view
            pygame.display.flip()  # Update the display

        pygame.quit()
