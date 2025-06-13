from source.level import Level
from source.player import Player
from source.constants import Constants
from source.camera import Camera


import pygame

from source.weapon import Weapon


class Game:
    def __init__(self):
        pygame.init()
        self.constants = Constants()  # Initialize constants
        self.screen = pygame.display.set_mode(
            self.constants.screen_dimensions, pygame.SRCALPHA
        )  # Set the screen size
        pygame.display.set_caption("KeiTV game")

        self.clock = pygame.time.Clock()

        self.object_group = pygame.sprite.Group()  # Create a group for level tiles
        self.background_group = (
            pygame.sprite.Group()
        )  # Create a group for background tiles
        self.level = Level(
            self.background_group, self.object_group, self.constants
        )  # Create a level with specified dimensions

        self.player = Player(
            50, 50, self.constants, self.level
        )  # Create a player at position (50, 50)
        self.player_group = pygame.sprite.GroupSingle(self.player)  # type: ignore

        self.weapon_group = pygame.sprite.GroupSingle()
        self.weapon = Weapon(self.weapon_group, self.constants, self.player)

        self.camera = Camera(
            self.constants, self.screen, self.level, self.player
        )  # Create a camera for the game
        self.weapon.set_camera(self.camera)  # Set the camera for the weapon

    def run(self):
        running = True

        maximum_frame_time = 1 + int(
            1 / self.constants.fps * 1000
        )  # Maximum frame time in milliseconds
        while running:
            dt = self.clock.tick(
                self.constants.fps
            )  # Get the time since the last frame in milliseconds

            if dt > maximum_frame_time:
                print(
                    f"Warning: Frame time {dt}ms exceeds target frame time {maximum_frame_time}ms."
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.object_group.update(dt)
            self.player_group.update(dt)
            self.weapon_group.update(dt)
            self.camera.update()

            self.camera.draw(
                self.background_group,
                self.object_group,
                self.player_group,
                self.weapon_group,
            )  # Draw camera view
            pygame.display.flip()  # Update the display

        pygame.quit()
