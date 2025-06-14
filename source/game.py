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

        self.player = Player(50, 50, self.constants)
        self.player_group = pygame.sprite.GroupSingle(self.player)  # type: ignore

        self.weapon_group = pygame.sprite.Group()
        self.weapon = Weapon(self.weapon_group, self.constants)
        self.projectile_group = pygame.sprite.Group()

        self.camera = Camera(self.constants, self.screen, self.level, self.player)

        self.hud = HUD(self.constants, self.player, self.weapon)
        self.hud_group = pygame.sprite.GroupSingle(self.hud)  # type: ignore

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.weapon.start_firing_projectiles()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.weapon.stop_firing_projectiles()
            elif event.type == pygame.MOUSEMOTION:
                new_mouse_pos = self.camera.from_screen_pos(event.pos)
                self.weapon.update_mouse_position(new_mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_w:
                    self.player.start_moving_up()
                elif event.key == pygame.K_s:
                    self.player.start_moving_down()
                elif event.key == pygame.K_a:
                    self.player.start_moving_left()
                elif event.key == pygame.K_d:
                    self.player.start_moving_right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.stop_moving_up()
                elif event.key == pygame.K_s:
                    self.player.stop_moving_down()
                elif event.key == pygame.K_a:
                    self.player.stop_moving_left()
                elif event.key == pygame.K_d:
                    self.player.stop_moving_right()

    def run(self):
        self.running = True

        maximum_frame_time = 1 + int(1 / self.constants.fps * 1000)
        while self.running:
            dt = self.clock.tick(self.constants.fps)

            if dt > maximum_frame_time:
                print(
                    f"Warning: Frame time {dt}ms exceeds target frame time {maximum_frame_time}ms."
                )

            self.handle_events()

            self.object_group.update(dt)
            self.player_group.update(dt, self.level)
            player_center = self.player.rect.center
            self.weapon_group.update(dt, player_center, self.projectile_group)
            self.projectile_group.update(dt, self.level.get_obstacles())
            self.hud_group.update()
            self.camera.update()

            self.camera.draw(
                self.background_group,
                self.hud_group,
                self.object_group,
                self.player_group,
                self.weapon_group,
                self.projectile_group,
            )
            pygame.display.flip()  # Update the display

        pygame.quit()
