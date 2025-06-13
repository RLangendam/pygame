import pygame
from source.camera import Camera
from source.constants import Constants
from source.player import Player
from source.projectile import Projectile


class Weapon(pygame.sprite.Sprite):
    def __init__(self, group, constants: Constants, player: Player):
        super().__init__(group)
        self.group = group
        image_dimensions = (constants.tile_size, constants.tile_size)
        self.image = pygame.Surface(image_dimensions, pygame.SRCALPHA)
        self.weapon_length = constants.tile_size
        self.weapon_width = int(constants.tile_size / 4)
        self.weapon_radius = int(constants.tile_size / 2)
        self.rect = self.image.get_rect()
        self.player = player
        self.ammo = 10
        self.firing_projectiles = False
        self.last_fired = 0

    def update(self, dt: int):
        mouse_x, mouse_y = self.camera.get_mouse_pos()
        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery
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
        center_x = self.player.rect.centerx + offset.x
        center_y = self.player.rect.centery + offset.y
        self.rect = self.image.get_rect(center=(center_x, center_y))

        self.update_firing_projectiles(direction, dt)

    def set_camera(self, camera: Camera):
        self.camera = camera

    def start_firing_projectiles(self):
        self.firing_projectiles = True

    def stop_firing_projectiles(self):
        # Logic to stop firing projectiles
        self.firing_projectiles = False

    def update_firing_projectiles(self, direction: pygame.math.Vector2, dt: int):
        self.last_fired += dt
        if self.firing_projectiles and self.ammo > 0 and self.last_fired > 500:
            Projectile(self.rect.center, direction, self.group, self.get_obstacles())
            self.ammo -= 1
            self.last_fired = 0

    def get_obstacles(self):
        return self.player.get_obstacles()
