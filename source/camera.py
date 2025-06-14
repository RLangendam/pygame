import pygame
from itertools import chain
from source.constants import Constants
from source.level import Level
from source.player import Player
from source.utils import clamp


class Camera(pygame.sprite.Sprite):
    def __init__(self, constants: Constants, *groups):
        super().__init__(*groups)
        self.constants = constants

        self.camera_image = pygame.Surface(constants.camera_dimensions, pygame.SRCALPHA)
        self.camera_rect = self.camera_image.get_rect()

        self.image = pygame.Surface(constants.screen_dimensions, pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(
        self,
        target: pygame.sprite.Sprite,
        level: Level,
        background_group,
        foreground_group,
        y_sorted_group,
    ):
        x = target.rect.centerx - int(self.camera_rect.width / 2)  # type: ignore
        y = target.rect.centery - int(self.camera_rect.height / 2)  # type: ignore
        delta_width = level.width - self.camera_rect.width
        delta_height = level.height - self.camera_rect.height
        x = clamp(x, 0, delta_width)
        y = clamp(y, 0, delta_height)
        self.camera_rect.topleft = (x, y)

        self.update_image(background_group, foreground_group, y_sorted_group)

    def update_image(self, background_group, foreground_group, y_sorted_group):
        self.camera_image.fill((0, 0, 0, 0))  # Clear the camera surface

        sprites = sorted(y_sorted_group, key=lambda s: s.rect.bottom)

        for sprite in chain(iter(background_group), sprites):
            # Draw each sprite at its position relative to the camera
            dx = sprite.rect.x - self.camera_rect.x
            dy = sprite.rect.y - self.camera_rect.y
            self.camera_image.blit(sprite.image, (dx, dy))

        foreground_group.draw(self.camera_image)

        screen_dimensions = (self.image.get_width(), self.image.get_height())
        pygame.transform.scale(self.camera_image, screen_dimensions, self.image)

    def from_screen_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        x = pos[0] * self.camera_rect.width // self.constants.screen_dimensions[0]
        y = pos[1] * self.camera_rect.height // self.constants.screen_dimensions[1]
        return x + self.camera_rect.x, y + self.camera_rect.y
