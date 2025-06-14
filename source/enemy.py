import pygame

from source.constants import Constants
from source.movable import Movable


class Enemy(Movable):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        tile_dimensions = (constants.tile_size, constants.tile_size)
        image = pygame.Surface(tile_dimensions, pygame.SRCALPHA)
        rect = image.get_rect(topleft=pos * constants.tile_size)
        super().__init__(image, rect, *groups)
        pygame.draw.circle(
            self.image,
            (0, 0, 0, 255),
            (constants.tile_size // 2, constants.tile_size // 2),
            constants.tile_size // 4,
        )
        self.health = 3
        self.movement_speed = 0.1

    def hit(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def update(self, dt: int, player_center: tuple[int, int], width, height, obstacles):
        target_x, target_y = player_center
        x = target_x - self.rect.centerx
        y = target_y - self.rect.centery
        direction = pygame.Vector2(x, y).normalize() * self.movement_speed * dt
        dx = int(direction.x)
        dy = int(direction.y)

        dx, dy = self.restrict_to_level_bounds(dx, dy, width, height)
        if dx == 0 and dy == 0:
            return

        other_obstacles = filter(lambda sprite: sprite != self, obstacles)
        dx, dy = self.move_avoiding_collisions(dx, dy, other_obstacles)
        if dx == 0 and dy == 0:
            return

        # Add player collision logic
