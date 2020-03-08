import numpy as np

from visualizer.sprite import Sprite, Animator
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
        self.speed = -0.1
        self.animator = Animator(self, "slime", 2)
        self.animator.start()

    def update(self, dt):
        super().update(dt)
        self.animator.update()

    def update_position_velocity(self, dt):
        super().update_position_velocity(dt)
        self.velocity[0] = self.speed

    def update_collisions(self, tiles, tile_array):
        collided = super().update_collisions(tiles, tile_array)
        if Direction.LEFT in collided or Direction.RIGHT in collided:
            self.speed = -self.speed
            self.flip()

enemies = {
    'G': Slime
}