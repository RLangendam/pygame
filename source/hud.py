import pygame


class HUD(pygame.sprite.Sprite):
    def __init__(self, constants, player, weapon):
        super().__init__()
        self.constants = constants
        self.player = player
        self.weapon = weapon
        self.image = pygame.Surface((80, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.font = pygame.font.Font(None, 14)

    def update(self):
        self.image.fill((0, 0, 0, 128))  # Semi-transparent background
        health_text = f"Health: {self.player.health}"
        ammo_text = f"Ammo: {self.weapon.ammo}"
        texts = [health_text, ammo_text]
        texts.extend(
            (f"{key}: {value}" for key, value in self.player.inventory.items())
        )

        surfaces = [self.font.render(text, False, (255, 255, 255)) for text in texts]

        for i, surface in enumerate(surfaces):
            self.image.blit(surface, (5, 5 + i * 15))
