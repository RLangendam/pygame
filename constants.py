FPS = 60  # Frames per second

TILE_SIZE = 32  # Size of each tile in pixels
HORIZONTAL_TILE_COUNT = 16
ASPECT_RATIO = 16 / 9
VERTICAL_TILE_COUNT = int(HORIZONTAL_TILE_COUNT / ASPECT_RATIO)

CAMERA_WIDTH = HORIZONTAL_TILE_COUNT * TILE_SIZE
CAMERA_HEIGHT = VERTICAL_TILE_COUNT * TILE_SIZE

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = int(SCREEN_WIDTH / ASPECT_RATIO)

LEVEL_WIDTH = 1000  # Width of the level in pixels
LEVEL_HEIGHT = 1000  # Height of the level in pixels


class Constants:
    def __init__(self):
        self.fps = FPS
        self.tile_size = TILE_SIZE
        self.camera_dimensions = (CAMERA_WIDTH, CAMERA_HEIGHT)
        self.screen_dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.level_width = LEVEL_WIDTH
        self.level_height = LEVEL_HEIGHT

        assert (
            self.screen_dimensions[1] == 720
        ), "Screen height must be 720 for a 16:9 aspect ratio with the given width."
