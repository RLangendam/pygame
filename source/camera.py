import pygame
from itertools import chain
from source.constants import Constants
from source.level import Level
from source.player import Player
from source.utils import clamp


class Camera:
    def __init__(
        self, constants: Constants, screen: pygame.Surface, level: Level, target: Player
    ):
        self.constants = constants
        self.screen = screen
        self.level = level
        self.target = target
        self.image = pygame.Surface(constants.camera_dimensions, pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        x = self.target.rect.centerx - int(self.rect.width / 2)
        y = self.target.rect.centery - int(self.rect.height / 2)
        delta_width = self.level.width - self.rect.width
        delta_height = self.level.height - self.rect.height
        x = clamp(x, 0, delta_width)
        y = clamp(y, 0, delta_height)
        self.rect.topleft = (x, y)

    def draw(self, background_group, hud_group, *y_sorted_sprite_groups):
        self.image.fill((0, 0, 0, 0))  # Clear the camera surface

        sprites = (sprite for group in y_sorted_sprite_groups for sprite in group)
        sprites = sorted(sprites, key=lambda s: s.rect.bottom)

        for sprite in chain(iter(background_group), sprites):
            # Draw each sprite at its position relative to the camera
            dx = sprite.rect.x - self.rect.x
            dy = sprite.rect.y - self.rect.y
            self.image.blit(sprite.image, (dx, dy))

        for sprite in hud_group:
            self.image.blit(sprite.image, sprite.rect.topleft)

        screen_dimensions = (self.screen.get_width(), self.screen.get_height())
        pygame.transform.scale(self.image, screen_dimensions, self.screen)

    def from_screen_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        x = pos[0] * self.rect.width // self.screen.get_width()
        y = pos[1] * self.rect.height // self.screen.get_height()
        return x + self.rect.x, y + self.rect.y
