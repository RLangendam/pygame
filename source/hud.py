import pygame


class HUD(pygame.sprite.Sprite):
    def __init__(self, constants, *groups):
        super().__init__(*groups)
        self.constants = constants
        self.image = pygame.Surface((90, 60), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.font = pygame.font.Font("assets/graphics/fonts/pixel.ttf", 10)

    def update(self, health: int, ammo: int, inventory: dict):
        self.image.fill((0, 0, 0, 128))  # Semi-transparent background
        health_text = f"Health: {health}"
        ammo_text = f"Ammo: {ammo}"
        texts = [health_text, ammo_text]
        texts.extend((f"{key}: {value}" for key, value in inventory.items()))

        surfaces = [self.font.render(text, False, (255, 255, 255)) for text in texts]

        for i, surface in enumerate(surfaces):
            self.image.blit(surface, (5, 5 + i * 15))
