import numpy as np

from .sprite import Sprite, Animator
from visualizer.util import *
from math import sqrt
from abc import ABC, abstractmethod

class Enemy(Sprite, ABC):
    @abstractmethod
    def update(self,dt):
        super().update(dt)

class Slime(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.speed = -0.2

    def update(self, dt):
        super().update(dt)

    def update_position_velocity(self, dt):
        super().update_position_velocity(dt)
        self.velocity[0] = self.speed

    def update_collisions(self, tiles, tile_array):
        collided = super().update_collisions(tiles, tile_array)

        if Direction.LEFT in collided:
            self.speed = -self.speed
        elif Direction.RIGHT in collided:
            self.speed = -self.speed

class Buzzard(Enemy):
    def __init__(self, *args):
        super().__init__(*args, gravity=False)
        self.speed = -0.0

    def update(self, dt):
        super().update(dt)

enemies = {
    'G': Slime,
    'B': Buzzard
}