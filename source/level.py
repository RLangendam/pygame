from itertools import chain
import pygame
from source.constants import Constants


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, background_group, object_group, x: int, y: int, size: int, char: str
    ):
        if char == "x":
            super().__init__(background_group)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            self.image.fill((255, 255, 255, 255))
            self.block = True
        elif char == " ":
            super().__init__(background_group)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            self.image.fill((100, 100, 100, 255))
            self.block = False
        elif char == "o":
            super().__init__(object_group)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            self.image.fill((0, 255, 0, 255))
            self.block = False
        elif char == "b":
            super().__init__(object_group)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            self.image.fill((0, 0, 255, 255))
            self.block = True
        else:
            raise ValueError(f"Unknown tile character: {char}")
        self.rect = self.image.get_rect(topleft=(x * size, y * size))


MAP = """xxxxxxxxxxxxxxxxxxxxxx
x                    x
x                    x
x       xxxxx        x
x                    x
x                    x
x    o  b  xxxxx     x
x                    x
x                    x
xxxxxxxxxxxxxxxxxxxxxx"""


class Level:
    def __init__(self, background_group, object_group, constants: Constants):
        characters = [list(row) for row in MAP.splitlines()]
        self.tiles = []
        for y, row in enumerate(characters):
            for x, char in enumerate(row):
                self.tiles.append(
                    Tile(
                        background_group, object_group, x, y, constants.tile_size, char
                    )
                )
        self.width = len(characters[0]) * constants.tile_size
        self.height = len(characters) * constants.tile_size
        self.background_group = background_group
        self.object_group = object_group

    def get_blocked_tile_rects(self):
        return (
            tile.rect
            for tile in chain(iter(self.background_group), iter(self.object_group))
            if tile.block
        )
