import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(
        self,
        start_pos: tuple[int, int],
        direction: pygame.Vector2,
        *groups,
    ):
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 255))
        self.rect = self.image.get_rect(center=start_pos)
        self.direction = direction.normalize()  # Normalize the direction vector
        self.speed = 1  # Speed of the projectile

    def update(self, dt: int, obstacles):
        # Move the projectile in the direction it was fired
        delta = self.direction * self.speed * dt
        self.rect.move_ip(delta.x, delta.y)

        colliders = pygame.sprite.spritecollide(self, obstacles, False)  # type: ignore
        for obstacle in colliders:
            if pygame.sprite.collide_mask(self, obstacle) is not None:
                obstacle.hit()
                self.kill()
