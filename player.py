from constants import Constants


import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, constants: Constants):
        super().__init__()
        self.image = pygame.Surface(
            (constants.tile_size, constants.tile_size)
        )  # Create a square surface
        pygame.draw.ellipse(self.image, (255, 0, 0), self.image.get_rect())
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt: int):
        # Update player logic here
        keys = pygame.key.get_pressed()  # Check for key presses
        if keys[pygame.K_LEFT]:
            self.rect.x -= int(200 * dt / 1000)
        if keys[pygame.K_RIGHT]:
            self.rect.x += int(200 * dt / 1000)
        if keys[pygame.K_UP]:
            self.rect.y -= int(200 * dt / 1000)
        if keys[pygame.K_DOWN]:
            self.rect.y += int(200 * dt / 1000)
