from source.constants import Constants
from source.level import Level
from source.player import Player
from source.utils import clamp


import pygame


class Camera:
    def __init__(self, constants: Constants, level: Level, player: Player):
        self.constants = constants
        self.level = level
        self.player = player
        self.image = pygame.Surface(
            constants.camera_dimensions
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

    def draw(self, surface: pygame.Surface, *sprite_groups):
        self.image.fill((0, 0, 0))  # Clear the camera surface
        for group in sprite_groups:
            for sprite in group:
                # Draw each sprite at its position relative to the camera
                self.image.blit(
                    sprite.image,
                    (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y),
                )
        pygame.transform.scale(
            self.image, (surface.get_width(), surface.get_height()), surface
        )  # Scale camera view to screen size
