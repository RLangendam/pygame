import pygame

NONE = 0
X = 1
Y = 2


class Movable(pygame.sprite.Sprite):
    def __init__(
        self, surface: pygame.Surface, rect: pygame.Rect, health: int, *groups
    ):
        super().__init__(*groups)  # type: ignore
        self.image = surface
        self.rect = rect
        self.health = health

    def move_avoiding_collisions(self, dx, dy, obstacles):
        self.rect.move_ip(dx, dy)
        blockers = pygame.sprite.spritecollide(self, obstacles, False)  # type: ignore
        if len(blockers) == 0:
            return dx, dy

        reverted = NONE
        for blocker in blockers:
            if pygame.sprite.collide_mask(self, blocker) is None:
                continue

            if dx == 0:
                self.rect.move_ip(0, -dy)
                return 0, 0
            if dy == 0:
                self.rect.move_ip(-dx, 0)
                return 0, 0

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

    def restrict_to_level_bounds(self, dx: int, dy: int, width: int, height: int):
        if dx != 0:
            new_x = self.rect.x + dx
            if new_x < 0 or new_x > width - self.rect.width:
                dx = 0
        if dy != 0:
            new_y = self.rect.y + dy
            if new_y < 0 or new_y > height - self.rect.height:
                dy = 0
        return dx, dy

    def hit(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.death()

    def death(self):
        pass
