import pygame
from source.clock import Clock
from source.display import Display
from source.hud import HUD
from source.level import Level
from source.constants import Constants
from source.camera import Camera
from source.weapon import Weapon


class Game:
    def __init__(self):
        pygame.init()
        self.constants = Constants()
        self.display = Display(self.constants)
        self.clock = Clock(self.constants)
        self.y_sorted_group = pygame.sprite.Group()
        self.statics_group = pygame.sprite.Group()
        self.dynamics_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.level = Level(
            self.background_group,
            self.dynamics_group,
            self.statics_group,
            self.y_sorted_group,
            self.constants,
        )
        self.player_group = self.level.get_player()
        self.player = self.player_group.sprite
        self.weapon_group = pygame.sprite.GroupSingle()
        self.weapon = Weapon(self.constants, self.weapon_group, self.y_sorted_group)
        self.projectile_group = pygame.sprite.Group()
        self.camera_group = pygame.sprite.GroupSingle()
        self.camera = Camera(self.constants, self.camera_group)
        self.hud_group = pygame.sprite.GroupSingle()
        self.hud = HUD(self.constants, self.hud_group)
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                new_mouse_pos = self.camera.from_screen_pos(event.pos)
                self.weapon.update_mouse_position(new_mouse_pos)
            else:
                self.player.handle(event)
                self.weapon.handle(event)

    def update_groups(self, dt):
        self.dynamics_group.update(dt)
        self.player_group.update(
            dt,
            self.level.width,
            self.level.height,
            self.level.get_obstacles(),
            self.level.get_items(),
        )
        self.level.get_enemies().update(
            dt,
            self.player,
            self.level.width,
            self.level.height,
            self.level.get_obstacles(),
        )
        self.weapon_group.update(
            dt, self.player.rect.center, self.projectile_group, self.y_sorted_group
        )
        self.projectile_group.update(dt, self.level.get_obstacles())
        self.hud_group.update(
            self.player.health, self.weapon.ammo, self.player.inventory
        )
        self.camera_group.update(
            self.player,
            self.level,
            self.background_group,
            self.hud_group,
            self.y_sorted_group,
        )

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick()
            self.handle_events()
            self.update_groups(dt)
            self.display.draw(self.camera_group)

        pygame.quit()
