from level import Level
from constants import Constants


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
        self.rect.x += int(d.x)
        self.rect.y += int(d.y)
