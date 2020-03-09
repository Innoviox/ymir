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

        self._hitbox = [0, 0, 1, 0.7]
        self.entity.double_sided = True

    def update(self, dt):
        super().update(dt)
        self.velocity[0] = self.speed

    def update_collisions(self, tiles, tile_array):
        collided = super().update_collisions(tiles, tile_array)

        if Direction.LEFT in collided or Direction.RIGHT in collided:
            self.speed = -self.speed
            self.entity.rotation_y += 180

    def die(self):
        super().die()

        self.animator.kill()
        self.speed = 0
        self.entity.fade_out(duration=1, delay=1)

    def collide(self, tile, direction):
        if not self.dead and 'Player' in str(type(tile)): # hack to get around importing Player
            if direction == Direction.UP:
                tile.velocity[1] = tile.jump_speed
                tile.can_jump = False
                self.die()
            else:
                self.controller.die()
        return False


class Slime(BasicEnemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, speed=-0.2)

class Buzzard(BasicEnemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, speed=0.2, gravity=False)
        self.animator.anim_every = 10

enemies = {
    'G': Slime,
    'B': Buzzard
}