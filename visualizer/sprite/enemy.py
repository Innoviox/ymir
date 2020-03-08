import numpy as np

from .sprite import Sprite, Animator
from visualizer.util import *
from math import sqrt
from abc import ABC, abstractmethod

class Enemy(Sprite, ABC):
    @abstractmethod
    def update(self,dt):
        super().update(dt)

class BasicEnemy(Enemy):
    def __init__(self, *args, **kwargs):
        self.speed = kwargs.pop("speed") or 0.1

        super().__init__(*args, **kwargs)


    def update(self, dt):
        super().update(dt)
        self.velocity[0] = self.speed

    def update_collisions(self, tiles, tile_array):
        collided = super().update_collisions(tiles, tile_array)

        if Direction.LEFT in collided:
            self.speed = -self.speed
        elif Direction.RIGHT in collided:
            self.speed = -self.speed

class Slime(BasicEnemy):
    def __init__(self, *args):
        super().__init__(*args, speed=-0.2)

class Buzzard(BasicEnemy):
    def __init__(self, *args):
        super().__init__(*args, speed=-0.2, gravity=False)

enemies = {
    'G': Slime,
    'B': Buzzard
}