import pygame
from source.constants import Constants


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, x: int, y: int, size: int, char: str):
        super().__init__(group)
        self.image = pygame.Surface((size, size))
        if char == "x":
            self.image.fill((255, 255, 255))
            self.block = True
        elif char == " ":
            self.image.fill((100, 100, 100))
            self.block = False
        else:
            raise ValueError(f"Unknown tile character: {char}")
        self.rect = self.image.get_rect(topleft=(x * size, y * size))


MAP = """xxxxxxxxxxxxxxxxxxxxxx
x                    x
x                    x
x       xxxxx        x
x                    x
x                    x
x          xxxxx     x
x                    x
x                    x
xxxxxxxxxxxxxxxxxxxxxx"""


class Level:
    def __init__(self, group, constants: Constants):
        characters = [list(row) for row in MAP.splitlines()]
        self.tiles = []
        for y, row in enumerate(characters):
            for x, char in enumerate(row):
                self.tiles.append(Tile(group, x, y, constants.tile_size, char))
        self.width = len(characters[0]) * constants.tile_size
        self.height = len(characters) * constants.tile_size
        self.group = group

    def get_blocked_tile_rects(self):
        return [tile.rect for tile in self.group if tile.block]
