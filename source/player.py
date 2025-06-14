import pygame
from source.level import Level
from source.constants import Constants


NONE = 0
X = 1
Y = 2


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, constants: Constants, level: Level):
        super().__init__()
        image_dimensions = (constants.tile_size, constants.tile_size)
        self.image = pygame.Surface(image_dimensions, pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 0, 0, 255), self.image.get_rect())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.level = level  # Store the level reference
        self.health = 100
        self.inventory = {"Item": 0}
        self.movement_x = 0
        self.movement_y = 0

    def update(self, dt: int):
        dx, dy = self.deltas_from_direction(dt)
        if dx == 0 and dy == 0:
            return

        dx, dy = self.restrict_to_level_bounds(dx, dy)
        if dx == 0 and dy == 0:
            return

        dx, dy = self.move_avoiding_collisions(dx, dy)
        if dx == 0 and dy == 0:
            return

        self.pickup_items()

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

    def get_obstacles(self):
        return self.level.get_obstacles()

    def move_avoiding_collisions(self, dx, dy):
        self.rect.move_ip(dx, dy)
        blockers = pygame.sprite.spritecollide(self, self.get_obstacles(), False)  # type: ignore
        if len(blockers) == 0:
            return dx, dy
        if dx == 0:
            self.rect.move_ip(0, -dy)
            return 0, 0
        if dy == 0:
            self.rect.move_ip(-dx, 0)
            return 0, 0

        reverted = NONE
        for blocker in blockers:
            if pygame.sprite.collide_mask(self, blocker) is None:
                continue

            if reverted & X == 0:
                self.rect.move_ip(-dx, 0)
                dx = 0
                reverted |= X
                if pygame.sprite.collide_mask(self, blocker) is None:
                    continue

            if reverted & Y == 0:
                self.rect.move_ip(0, -dy)
                dy = 0
                reverted |= Y
                if pygame.sprite.collide_mask(self, blocker) is None:
                    continue

            assert reverted == X | Y, "Reverted should be both X and Y"
            break

        return dx, dy

    def restrict_to_level_bounds(self, dx, dy):
        if dx != 0:
            new_x = self.rect.x + dx
            if new_x < 0 or new_x > self.level.width - self.rect.width:
                dx = 0
        if dy != 0:
            new_y = self.rect.y + dy
            if new_y < 0 or new_y > self.level.height - self.rect.height:
                dy = 0
        return dx, dy

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

    def pickup_items(self):
        items = pygame.sprite.spritecollide(self, self.level.get_items(), False)  # type: ignore
        for item in items:
            item.pickup(self.inventory)
