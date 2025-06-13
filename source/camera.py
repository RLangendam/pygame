from itertools import chain
from source.constants import Constants
from source.level import Level
from source.player import Player
from source.utils import clamp


import pygame


class Camera:
    def __init__(
        self, constants: Constants, screen: pygame.Surface, level: Level, player: Player
    ):
        self.constants = constants
        self.screen = screen
        self.level = level
        self.player = player
        self.image = pygame.Surface(
            constants.camera_dimensions, pygame.SRCALPHA
        )  # Create a surface for the camera view
        self.rect = self.image.get_rect()

    def update(self):
        x = clamp(
            self.player.rect.centerx - int(self.rect.width / 2),
            0,
            self.level.width - self.rect.width,
        )
        y = clamp(
            self.player.rect.centery - int(self.rect.height / 2),
            0,
            self.level.height - self.rect.height,
        )

        self.rect.topleft = (x, y)

    def draw(self, background_group, *sprite_groups):
        self.image.fill((0, 0, 0, 0))  # Clear the camera surface

        sprites = (sprite for group in sprite_groups for sprite in group)
        sprites = sorted(sprites, key=lambda s: s.rect.y)

        for sprite in chain(iter(background_group), sprites):
            # Draw each sprite at its position relative to the camera
            self.image.blit(
                sprite.image,
                (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y),
            )
        pygame.transform.scale(
            self.image, (self.screen.get_width(), self.screen.get_height()), self.screen
        )  # Scale camera view to screen size

    def from_screen_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        x = pos[0] * self.rect.width // self.screen.get_width()
        y = pos[1] * self.rect.height // self.screen.get_height()
        return x + self.rect.x, y + self.rect.y
