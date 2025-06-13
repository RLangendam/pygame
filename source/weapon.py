import pygame

from source.camera import Camera
from source.constants import Constants
from source.player import Player


class Weapon(pygame.sprite.Sprite):
    def __init__(self, group, constants: Constants, player: Player):
        super().__init__(group)
        self.image = pygame.Surface(
            (constants.tile_size, constants.tile_size), pygame.SRCALPHA
        )
        self.weapon_length = constants.tile_size
        self.weapon_width = int(constants.tile_size / 4)
        self.weapon_radius = int(constants.tile_size / 2)
        self.rect = self.image.get_rect()
        self.player = player

    def update(self, dt: int):
        mouse_x, mouse_y = self.camera.from_screen_pos(
            pygame.mouse.get_pos()
        )  # Get the mouse position
        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery
        # Protect against division by zero during normalization
        if dx == 0 and dy == 0:
            return

        self.image.fill((0, 0, 0, 0))  # Clear the weapon image
        # Calculate the mouse position relative to the weapon's center
        weapon_center = pygame.math.Vector2(
            self.image.get_width() // 2, self.image.get_height() // 2
        )
        mouse_pos_on_image = weapon_center + pygame.math.Vector2(dx, dy)
        pygame.draw.line(
            self.image,
            (255, 0, 0, 255),
            weapon_center,
            mouse_pos_on_image,
            self.weapon_width,
        )

        relative_mouse_pos = pygame.math.Vector2(dx, dy)
        offset = relative_mouse_pos.normalize() * self.weapon_radius
        center_x = self.player.rect.centerx + offset.x
        center_y = self.player.rect.centery + offset.y
        self.rect = self.image.get_rect(center=(center_x, center_y))

    def set_camera(self, camera: Camera):
        self.camera = camera
