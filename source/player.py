from source.level import Level
from source.constants import Constants


import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, constants: Constants, level: Level):
        super().__init__()
        self.image = pygame.Surface(
            (constants.tile_size, constants.tile_size)
        )  # Create a square surface
        pygame.draw.ellipse(self.image, (255, 0, 0), self.image.get_rect())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.level = level  # Store the level reference

    def update(self, dt: int):
        # Update player logic here
        keys = pygame.key.get_pressed()  # Check for key presses
        distance = int(200 * dt / 1000)  # Calculate distance to move based on dt
        d = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            d.x -= distance
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            d.x += distance
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            d.y -= distance
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            d.y += distance
        if d.length() > 0:
            d = d.normalize() * distance

        if (
            self.rect.x + d.x < 0
            or self.rect.x + d.x > self.level.width - self.rect.width
        ):
            d.x = 0
        if (
            self.rect.y + d.y < 0
            or self.rect.y + d.y > self.level.height - self.rect.height
        ):
            d.y = 0

        dx = int(d.x)
        dy = int(d.y)
        new_rect = self.rect.move(dx, dy)
        for tile_rect in self.level.get_blocked_tile_rects():
            if new_rect.colliderect(tile_rect):
                new_rect_x = self.rect.move(dx, 0)
                new_rect_y = self.rect.move(0, dy)
                if new_rect_x.colliderect(tile_rect):
                    dx = 0
                    if dy == 0:
                        break
                if new_rect_y.colliderect(tile_rect):
                    dy = 0
                    if dx == 0:
                        break

        if dx != 0:
            self.rect.x += dx
        if dy != 0:
            self.rect.y += dy

        self.weapon.update(dt)

    def set_weapon(self, weapon):
        self.weapon = weapon
