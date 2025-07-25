import pygame
from source.constants import Constants
from source.projectile import Projectile


class Weapon(pygame.sprite.Sprite):
    def __init__(self, constants: Constants, *groups):
        super().__init__(*groups)
        image_dimensions = (constants.tile_size, constants.tile_size)
        self.image = pygame.Surface(image_dimensions, pygame.SRCALPHA)
        self.weapon_length = constants.tile_size
        self.weapon_width = int(constants.tile_size / 4)
        self.weapon_radius = int(constants.tile_size / 2)
        self.rect = self.image.get_rect()
        self.ammo = 10
        self.firing_projectiles = False
        self.last_fired = 0
        self.mouse_pos = (0, 0)

    def update_mouse_position(self, mouse_pos: tuple[int, int]):
        self.mouse_pos = mouse_pos

    def update(self, dt: int, center: tuple[int, int], *groups):
        mouse_x, mouse_y = self.mouse_pos
        center_x, center_y = center
        dx = mouse_x - center_x
        dy = mouse_y - center_y
        # Protect against division by zero during normalization
        if dx == 0 and dy == 0:
            return

        self.image.fill((0, 0, 0, 0))
        # Calculate the mouse position relative to the weapon's center
        weapon_center = pygame.math.Vector2(
            self.image.get_width(), self.image.get_height()
        )
        weapon_center = weapon_center / 2
        direction = pygame.math.Vector2(dx, dy)
        mouse_pos_on_image = weapon_center + direction
        pygame.draw.line(
            self.image,
            (255, 0, 0, 255),
            weapon_center,
            mouse_pos_on_image,
            self.weapon_width,
        )

        relative_mouse_pos = pygame.math.Vector2(dx, dy)
        offset = relative_mouse_pos.normalize() * self.weapon_radius
        center_x += offset.x
        center_y += offset.y
        self.rect = self.image.get_rect(center=(center_x, center_y))

        self.update_firing_projectiles(direction, dt, *groups)

    def handle(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.firing_projectiles = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.firing_projectiles = False

    def update_firing_projectiles(
        self, direction: pygame.math.Vector2, dt: int, *groups
    ):
        self.last_fired += dt
        if self.firing_projectiles and self.ammo > 0 and self.last_fired > 500:
            Projectile(self.rect.center, direction, *groups)
            self.ammo -= 1
            self.last_fired = 0
