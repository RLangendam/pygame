import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(
        self,
        start_pos: tuple[int, int],
        direction: pygame.Vector2,
        group,
        obstacle_group,
    ):
        super().__init__(group)
        self.obstacle_group = obstacle_group
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 255))
        self.rect = self.image.get_rect(center=start_pos)
        self.direction = direction.normalize()  # Normalize the direction vector
        self.speed = 1  # Speed of the projectile

    def update(self, dt: int):
        # Move the projectile in the direction it was fired
        delta = self.direction * self.speed * dt
        self.rect.move_ip(delta.x, delta.y)

        obstacles = pygame.sprite.spritecollide(self, self.obstacle_group, False)  # type: ignore
        for obstacle in obstacles:
            if pygame.sprite.collide_mask(self, obstacle) is not None:
                obstacle.hit()
                self.kill()
