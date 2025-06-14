from source.constants import Constants


import pygame


class Clock:
    def __init__(self, constants: Constants):
        self.clock = pygame.time.Clock()
        self.constants = constants
        self.maximum_frame_time = 1 + int(1 / self.constants.fps * 1000)

    def tick(self) -> int:
        dt = self.clock.tick(self.constants.fps)
        if dt > self.maximum_frame_time:
            print(
                f"Warning: Frame time {dt}ms exceeds target frame time {self.maximum_frame_time}ms."
            )
        return dt
