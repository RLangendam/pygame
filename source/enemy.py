import pygame

from source.constants import Constants
from source.movable import Movable


class Enemy(Movable):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        tile_dimensions = (constants.tile_size, constants.tile_size)
        image = pygame.Surface(tile_dimensions, pygame.SRCALPHA)
        rect = image.get_rect(topleft=pos * constants.tile_size)
        super().__init__(image, rect, 3, *groups)
        pygame.draw.circle(
            self.image,
            (0, 0, 0, 255),
            (constants.tile_size // 2, constants.tile_size // 2),
            constants.tile_size // 4,
        )
        self.movement_speed = 0.1
        self.last_hit = 0

    def death(self):
        self.kill()

    def update(self, dt: int, player: Movable, width, height, obstacles):
        self.last_hit += dt

        if (
            pygame.sprite.collide_rect(self, player)
            and pygame.sprite.collide_mask(self, player) is not None
        ):
            self.touch_player(player)
            return

        target_x, target_y = player.rect.center
        x = target_x - self.rect.centerx
        y = target_y - self.rect.centery
        direction = pygame.Vector2(x, y).normalize() * self.movement_speed * dt
        dx = int(direction.x)
        dy = int(direction.y)

        dx, dy = self.restrict_to_level_bounds(dx, dy, width, height)
        if dx == 0 and dy == 0:
            return

        other_obstacles = filter(lambda sprite: sprite != self, obstacles)
        self.move_avoiding_collisions(dx, dy, other_obstacles)

    def touch_player(self, player: Movable):
        if self.last_hit >= 1000:
            player.hit(5)
            self.last_hit = 0
