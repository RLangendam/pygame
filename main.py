import pygame

FPS = 60  # Frames per second
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Create a square surface
        self.image.fill((255, 0, 0))  # Fill it with red color
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("KeiTV game")

    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player_group = pygame.sprite.GroupSingle(player)

    running = True
    while running:
        dt = clock.tick(FPS)  # Limit to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player
        player_group.update(dt)

        screen.fill((0, 0, 0))  # Fill the screen with black
        player_group.draw(screen)
        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()