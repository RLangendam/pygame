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

    def update(self, dt: int):
        x, y = self.get_movement_direction()

        dx, dy = self.deltas_from_direction(x, y, dt)
        if dx == 0 and dy == 0:
            return

        dx, dy = self.restrict_to_level_bounds(dx, dy)
        if dx == 0 and dy == 0:
            return

        self.move_avoiding_collisions(dx, dy)

    def move_avoiding_collisions(self, dx, dy):
        self.rect.move_ip(dx, dy)
        blockers = pygame.sprite.spritecollide(self, self.level.get_blockers(), False)  # type: ignore
        if len(blockers) == 0:
            return
        if dx == 0:
            self.rect.move_ip(0, -dy)
            return
        if dy == 0:
            self.rect.move_ip(-dx, 0)
            return

        reverted = NONE
        for blocker in blockers:
            if pygame.sprite.collide_mask(self, blocker) is None:
                continue

            if reverted & X == 0:
                self.rect.move_ip(-dx, 0)
                reverted |= X
                if pygame.sprite.collide_mask(self, blocker) is None:
                    continue

            if reverted & Y == 0:
                self.rect.move_ip(0, -dy)
                reverted |= Y
                if pygame.sprite.collide_mask(self, blocker) is None:
                    continue

            assert reverted == X | Y, "Reverted should be both X and Y"
            break

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

    def get_movement_direction(self):
        keys = pygame.key.get_pressed()
        x, y = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y += 1
        return x, y

    def deltas_from_direction(self, x: int, y: int, dt: int) -> tuple[int, int]:
        if x != 0 and y != 0:
            # Diagonal movement: 0.141 = sqrt(2) * 200 / 1000
            distance = int(0.141 * dt)
        elif x == 0 and y == 0:
            return 0, 0  # No movement
        else:
            distance = int(0.2 * dt)  # Calculate distance to move based on dt

        dx = x * distance
        dy = y * distance
        return dx, dy
