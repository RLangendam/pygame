import pygame

FPS = 60  # Frames per second

TILE_SIZE = 32  # Size of each tile in pixels
HORIZONTAL_TILE_COUNT = 16
ASPECT_RATIO = 16 / 9
VERTICAL_TILE_COUNT = int(HORIZONTAL_TILE_COUNT / ASPECT_RATIO)

CAMERA_WIDTH = HORIZONTAL_TILE_COUNT * TILE_SIZE
CAMERA_HEIGHT = VERTICAL_TILE_COUNT * TILE_SIZE

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = int(SCREEN_WIDTH / ASPECT_RATIO)

assert SCREEN_HEIGHT == 720, "Screen height must be 1080 for a 16:9 aspect ratio with the given width."

LEVEL_WIDTH = 1000  # Width of the level in pixels
LEVEL_HEIGHT = 1000  # Height of the level in pixels

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))  # Create a square surface
        pygame.draw.ellipse(self.image, (255, 0, 0), self.image.get_rect())
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        # Update player logic here
        keys = pygame.key.get_pressed()  # Check for key presses
        if keys[pygame.K_LEFT]:
            self.rect.x -= 200 * dt / 1000
        if keys[pygame.K_RIGHT]:
            self.rect.x += 200 * dt / 1000  
        if keys[pygame.K_UP]:
            self.rect.y -= 200 * dt / 1000  
        if keys[pygame.K_DOWN]:
            self.rect.y += 200 * dt / 1000

class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.image = pygame.Surface((width, height))  # Create a surface for the camera view

    def update(self, target, level_width, level_height):
        x = target.rect.centerx - int(self.rect.width / 2)
        y = target.rect.centery - int(self.rect.height / 2)

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if self.rect.bottomright[0] > LEVEL_WIDTH:
            x = LEVEL_WIDTH - self.rect.width
        if self.rect.bottomright[1] > LEVEL_HEIGHT:
            y = LEVEL_HEIGHT - self.rect.height

        self.rect.topleft = (x, y)


    def draw(self, surface, *sprite_groups):
        self.image.fill((0, 0, 0))  # Clear the camera surface
        for group in sprite_groups:
            for sprite in group:
                # Draw each sprite at its position relative to the camera
                self.image.blit(sprite.image, (sprite.rect.x-self.rect.x, sprite.rect.y-self.rect.y)) # Gebruik de source surface rect als 3e argument
        pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT), surface)  # Scale camera view to screen size

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("KeiTV game")

    clock = pygame.time.Clock()

    player = Player(50, 50)  # Create a player at position (50, 50)
    player_group = pygame.sprite.GroupSingle(player)

    camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT)

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player
        player_group.update(dt)
        camera.update(player, LEVEL_WIDTH, LEVEL_HEIGHT)

        camera.draw(screen, player_group)  # Draw camera view
        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()