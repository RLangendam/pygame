import pygame
from source.constants import Constants
from source.enemy import Enemy
from source.player import Player


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        super().__init__(*groups)
        tile_dimensions = (constants.tile_size, constants.tile_size)
        self.image = pygame.Surface(tile_dimensions, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos * constants.tile_size)

    def hit(self, damage: int):
        pass


class Wall(Tile):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        super().__init__(pos, constants, *groups)
        self.image.fill((200, 200, 200, 255))  # Gray for walls


class Floor(Tile):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        super().__init__(pos, constants, *groups)
        self.image.fill((150, 150, 150, 255))  # Darker gray for floors


class Decoration(Tile):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        super().__init__(pos, constants, *groups)
        pygame.draw.circle(
            self.image,
            (0, 255, 0, 255),
            (constants.tile_size // 2, constants.tile_size // 2),
            constants.tile_size // 4,
        )


class Obstacle(Tile):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        super().__init__(pos, constants, *groups)
        pygame.draw.circle(
            self.image,
            (0, 0, 255, 255),
            (constants.tile_size // 2, constants.tile_size // 2),
            constants.tile_size // 4,
        )


class Item(Tile):
    def __init__(self, pos: pygame.Vector2, constants: Constants, *groups):
        super().__init__(pos, constants, *groups)
        pygame.draw.rect(
            self.image,
            (255, 255, 0, 255),
            (
                constants.tile_size // 4,
                constants.tile_size // 4,
                constants.tile_size // 2,
                constants.tile_size // 2,
            ),
        )

    def pickup(self, inventory: dict):
        inventory["Item"] += 1
        self.kill()


MAP = """xxxxxxxx  xxxxxxxxxxxx
x                    x
x         i          x
x       xxxxx        x
   p              e   
                      
x    o  b  xxxxx     x
x                    x
x                    x
xxxxxxxxxxx  xxxxxxxxx"""


class Level:
    def __init__(
        self,
        background_group,
        dynamics_group,
        statics_group,
        y_sorted_group,
        constants: Constants,
    ):
        characters = [list(row) for row in MAP.splitlines()]
        self.tiles = []
        self.obstacles_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        for y, row in enumerate(characters):
            for x, char in enumerate(row):
                pos = pygame.Vector2(x, y)
                sprites = []
                if char == "x":
                    sprite = Wall(
                        pos, constants, background_group, self.obstacles_group
                    )
                    sprites.append(sprite)
                elif char == " ":
                    sprite = Floor(pos, constants, background_group)
                    sprites.append(sprite)
                elif char == "o":
                    sprite = Decoration(pos, constants, statics_group, y_sorted_group)
                    sprites.append(sprite)
                    sprite = Floor(pos, constants, background_group)
                    sprites.append(sprite)
                elif char == "b":
                    sprite = Obstacle(
                        pos,
                        constants,
                        self.obstacles_group,
                        statics_group,
                        y_sorted_group,
                    )
                    sprites.append(sprite)
                    sprite = Floor(pos, constants, background_group)
                    sprites.append(sprite)
                elif char == "i":
                    sprite = Item(
                        pos, constants, self.item_group, statics_group, y_sorted_group
                    )
                    sprites.append(sprite)
                    sprite = Floor(pos, constants, background_group)
                    sprites.append(sprite)
                elif char == "e":
                    sprite = Enemy(
                        pos,
                        constants,
                        self.enemies_group,
                        y_sorted_group,
                        self.obstacles_group,
                    )
                    sprites.append(sprite)
                    sprite = Floor(pos, constants, background_group)
                    sprites.append(sprite)
                elif char == "p":
                    sprite = Player(
                        x * constants.tile_size,
                        y * constants.tile_size,
                        constants,
                        self.player_group,
                        y_sorted_group,
                    )
                    sprites.append(sprite)
                    sprite = Floor(pos, constants, background_group)
                    sprites.append(sprite)
                else:
                    raise ValueError(f"Unknown tile character: {char}")

                for sprite in sprites:
                    sprite.mask = pygame.mask.from_surface(sprite.image)
                self.tiles.extend(sprites)

        self.width = len(characters[0]) * constants.tile_size
        self.height = len(characters) * constants.tile_size

    def get_obstacles(self):
        return self.obstacles_group

    def get_items(self):
        return self.item_group

    def get_enemies(self):
        return self.enemies_group

    def get_player(self):
        return self.player_group
