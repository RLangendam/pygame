import pygame
from source.level import Level
from source.constants import Constants
from source.movable import Movable


class Player(Movable):
    def __init__(self, x: int, y: int, constants: Constants, *groups):
        image_dimensions = (constants.tile_size, constants.tile_size)
        image = pygame.Surface(image_dimensions, pygame.SRCALPHA)
        rect = image.get_rect(topleft=(x, y))
        super().__init__(image, rect, 100, *groups)
        pygame.draw.ellipse(self.image, (255, 0, 0, 255), self.image.get_rect())
        self.inventory = {"Item": 0}
        self.movement_x = 0
        self.movement_y = 0

    def update(self, dt: int, level: Level):
        dx, dy = self.deltas_from_direction(dt)
        if dx == 0 and dy == 0:
            return

        dx, dy = self.restrict_to_level_bounds(dx, dy, level.width, level.height)
        if dx == 0 and dy == 0:
            return

        dx, dy = self.move_avoiding_collisions(dx, dy, level.get_obstacles())
        if dx == 0 and dy == 0:
            return

        self.pickup_items(level.get_items())

    def start_moving_up(self):
        self.movement_y -= 1

    def start_moving_down(self):
        self.movement_y += 1

    def start_moving_left(self):
        self.movement_x -= 1

    def start_moving_right(self):
        self.movement_x += 1

    def stop_moving_up(self):
        self.movement_y += 1

    def stop_moving_down(self):
        self.movement_y -= 1

    def stop_moving_left(self):
        self.movement_x += 1

    def stop_moving_right(self):
        self.movement_x -= 1

    def deltas_from_direction(self, dt: int) -> tuple[int, int]:
        if self.movement_x != 0 and self.movement_y != 0:
            # Diagonal movement: 0.141 = sqrt(2) * 200 / 1000
            distance = int(0.141 * dt)
        elif self.movement_x == 0 and self.movement_y == 0:
            return 0, 0  # No movement
        else:
            distance = int(0.2 * dt)  # Calculate distance to move based on dt

        dx = self.movement_x * distance
        dy = self.movement_y * distance
        return dx, dy

    def pickup_items(self, items):
        items = pygame.sprite.spritecollide(self, items, False)  # type: ignore
        for item in items:
            item.pickup(self.inventory)

    def death(self):
        print("Game over")
