from itertools import chain
import pygame
from source.constants import Constants


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, pos: pygame.Vector2, constants: Constants):
        super().__init__(group)
        self.image = pygame.Surface(
            (constants.tile_size, constants.tile_size), pygame.SRCALPHA
        )
        self.rect = self.image.get_rect(topleft=pos * constants.tile_size)
        self.is_blocking = False  # Default to not blocking

    def blocks(self) -> bool:
        return self.is_blocking


class Wall(Tile):
    def __init__(self, background_group, pos: pygame.Vector2, constants: Constants):
        super().__init__(background_group, pos, constants)
        self.is_blocking = True
        self.image.fill((200, 200, 200, 255))  # Gray for walls


class Floor(Tile):
    def __init__(self, background_group, pos: pygame.Vector2, constants: Constants):
        super().__init__(background_group, pos, constants)
        self.image.fill((150, 150, 150, 255))  # Darker gray for floors


class Decoration(Tile):
    def __init__(self, background_group, pos: pygame.Vector2, constants: Constants):
        super().__init__(background_group, pos, constants)
        pygame.draw.circle(
            self.image,
            (0, 255, 0, 255),
            (constants.tile_size // 2, constants.tile_size // 2),
            constants.tile_size // 4,
        )


class Obstacle(Tile):
    def __init__(self, object_group, pos: pygame.Vector2, constants: Constants):
        super().__init__(object_group, pos, constants)
        self.is_blocking = True
        pygame.draw.circle(
            self.image,
            (0, 0, 255, 255),
            (constants.tile_size // 2, constants.tile_size // 2),
            constants.tile_size // 4,
        )


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
                pos = pygame.Vector2(x, y)
                sprites = []
                if char == "x":
                    sprite = Wall(background_group, pos, constants)
                    sprites.append(sprite)
                elif char == " ":
                    sprite = Floor(background_group, pos, constants)
                    sprites.append(sprite)
                elif char == "o":
                    sprite = Decoration(object_group, pos, constants)
                    sprites.append(sprite)
                    sprite = Floor(background_group, pos, constants)
                    sprites.append(sprite)
                elif char == "b":
                    sprite = Obstacle(object_group, pos, constants)
                    sprites.append(sprite)
                    sprite = Floor(background_group, pos, constants)
                    sprites.append(sprite)
                else:
                    raise ValueError(f"Unknown tile character: {char}")

                self.tiles.extend(sprites)

        self.width = len(characters[0]) * constants.tile_size
        self.height = len(characters) * constants.tile_size
        self.background_group = background_group
        self.object_group = object_group

    def get_blocked_tile_rects(self):
        return (
            tile.rect
            for tile in chain(iter(self.background_group), iter(self.object_group))
            if tile.blocks()
        )
