import pygame
from source.hud import HUD
from source.level import Level
from source.player import Player
from source.constants import Constants
from source.camera import Camera
from source.weapon import Weapon


class Game:
    def __init__(self):
        pygame.init()
        self.constants = Constants()  # Initialize constants
        self.screen = pygame.display.set_mode(
            self.constants.screen_dimensions, pygame.SRCALPHA
        )
        pygame.display.set_caption("KeiTV game")

        self.clock = pygame.time.Clock()

        self.object_group = pygame.sprite.Group()  # Create a group for level tiles
        self.background_group = pygame.sprite.Group()
        self.level = Level(self.background_group, self.object_group, self.constants)

        self.player = Player(50, 50, self.constants, self.level)
        self.player_group = pygame.sprite.GroupSingle(self.player)  # type: ignore

        self.weapon_group = pygame.sprite.Group()
        self.weapon = Weapon(self.weapon_group, self.constants, self.player)

        self.camera = Camera(self.constants, self.screen, self.level, self.player)
        self.weapon.set_camera(self.camera)  # Set the camera for the weapon

        self.hud = HUD(self.constants, self.player, self.weapon)
        self.hud_group = pygame.sprite.GroupSingle(self.hud)  # type: ignore

    def run(self):
        running = True

        maximum_frame_time = 1 + int(1 / self.constants.fps * 1000)
        while running:
            dt = self.clock.tick(self.constants.fps)

            if dt > maximum_frame_time:
                print(
                    f"Warning: Frame time {dt}ms exceeds target frame time {maximum_frame_time}ms."
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.weapon.start_firing_projectiles()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.weapon.stop_firing_projectiles()

            self.object_group.update(dt)
            self.player_group.update(dt)
            self.weapon_group.update(dt)
            self.hud_group.update()
            self.camera.update()

            self.camera.draw(
                self.background_group,
                self.hud_group,
                self.object_group,
                self.player_group,
                self.weapon_group,
            )
            pygame.display.flip()  # Update the display

        pygame.quit()
