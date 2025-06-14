from source.constants import Constants


import pygame


class Display:
    def __init__(self, constants: Constants):
        self.screen = pygame.display.set_mode(
            constants.screen_dimensions, pygame.SRCALPHA
        )
        pygame.display.set_caption("KeiTV game")

    def draw(self, group):
        group.draw(self.screen)
        pygame.display.flip()
