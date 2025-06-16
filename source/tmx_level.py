import os
import pygame
import pytmx
import time

from source.constants import Constants
from source.clock import Clock


class Image:
    def __init__(self, image, path):
        self.image = image
        self.path = path


class PlainSprite(pygame.sprite.DirtySprite):
    def __init__(self, constants: Constants, tile, x: int, y: int, *groups):
        super().__init__(*groups)
        self.constants = constants
        self.tile = tile
        self.image = pygame.Surface(
            (constants.tile_size, constants.tile_size), pygame.SRCALPHA
        )
        self.rect = self.image.get_rect(
            topleft=(x * constants.tile_size, y * constants.tile_size)
        )
        self.update_image(0, 0)

    def update_image(self, row: int, column: int):
        self.image.blit(
            self.tile.image.image,
            (0, 0),
            area=self.tile.rect.move(
                row * self.constants.tile_size, column * self.constants.tile_size
            ),
        )


class Water(PlainSprite):
    def __init__(self, constants: Constants, tile, x: int, y: int, *groups):
        super().__init__(constants, tile, x, y, *groups)
        self.time_remaining = self.animation_time = 0.5
        self.sprite_index = 0

    def update(self, dt: float):
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.sprite_index += 1
            if self.sprite_index > 3:
                self.sprite_index = 0
            self.update_image(0, self.sprite_index)
            self.time_remaining = self.animation_time


sprite_map = {"Water": Water}


class Tile:
    def __init__(self, constants: Constants, image: Image, rect: pygame.Rect):
        self.constants = constants
        self.image = image
        self.rect = rect

    def create_sprite(self, x: int, y: int) -> pygame.sprite.DirtySprite:
        name = os.path.basename(self.image.path)
        ctor = sprite_map.get(name, PlainSprite)
        return ctor(self.constants, self, x, y)


class YSortedLayeredDirty(pygame.sprite.LayeredDirty):
    def __init__(self, constants: Constants, *sprites, **kwargs):
        super().__init__(*sprites, **kwargs)
        self._last_time = time.time()
        self._update_time_threshold = 1 / constants.fps  # Approx 60 FPS
        self._clip = None  # Store latest clip for full redraw case

    def draw(self, surface, bgsurf=None, special_flags=None):
        now = time.time()
        self._use_update = (now - self._last_time) < self._update_time_threshold
        self._last_time = now

        dirty = []

        layers = {}
        for sprite in self.sprites():
            layer = self.get_layer_of_sprite(sprite)
            layers.setdefault(layer, []).append(sprite)

        for layer in sorted(layers):
            # Y-sort by rect.bottom within layer
            for spr in sorted(layers[layer], key=lambda s: s.rect.bottom):
                if spr.dirty:
                    rect = surface.blit(spr.image, spr.rect)
                    dirty.append(rect)
                    spr.dirty = 0  # mark clean

        # If using update optimization, return individual rects
        if self._use_update:
            return dirty
        else:
            # Return a single rect covering the whole screen (like LayeredDirty)
            self._clip = surface.get_clip()
            return [self._clip]


class TMXLevel:
    def __init__(self, constants: Constants, path: str):
        self.constants = constants
        map = pytmx.TiledMap(path)
        tiles = self.get_tiles(map)
        self.background, self.y_sorted, self.foreground = self.get_sprites(map, tiles)

    def update(self, *args, **kwargs):
        self.background.update(*args, **kwargs)
        self.y_sorted.update(*args, **kwargs)
        self.foreground.update(*args, **kwargs)

    def draw(self, surface: pygame.Surface):
        result = self.background.draw(surface)
        result.extend(self.y_sorted.draw(surface))
        result.extend(self.foreground.draw(surface))
        return result

    def get_sprites(self, map, tiles):
        background = pygame.sprite.LayeredDirty()
        y_sorted = YSortedLayeredDirty(self.constants)
        foreground = pygame.sprite.LayeredDirty()
        for layer_index, layer in enumerate(map.layers):
            class_name = None
            if hasattr(layer, "class"):
                class_name = getattr(layer, "class")
            if class_name == "Foreground":
                group = foreground
            elif class_name == "Background":
                group = background
            else:
                group = y_sorted
            if isinstance(layer, pytmx.TiledTileLayer):
                for y, row in enumerate(layer.data):
                    for x, tile_index in enumerate(row):
                        tile = tiles.get(tile_index)
                        if tile is not None:
                            sprite = tile.create_sprite(x, y)
                            group.add(sprite, layer=layer_index)
        return (background, y_sorted, foreground)

    def get_tiles(self, map):
        images = dict()
        tiles = dict()
        for image_index, image in enumerate(map.images):
            if image is not None:
                path, (x, y, w, h), _ = image  # type: ignore
                rect = pygame.Rect(x, y, w, h)
                found_image = images.get(path)
                if found_image is None:
                    image = pygame.image.load(path)
                    found_image = images[path] = Image(image, path)
                found_tile = tiles.get(image_index)
                assert found_tile is None
                tile = Tile(self.constants, found_image, rect)
                tiles[image_index] = tile
        return tiles


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA)
    constants = Constants()
    constants.tile_size = 16
    level = TMXLevel(constants, "assets/graphics/levels/temp/demo.tmx")

    clock = Clock(constants)
    running = True
    while running:
        dt = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        level.update(dt)

        rects = level.draw(screen)
        pygame.display.update(rects)

    # pygame.display.flip()
    # input("Press enter to stop.")
