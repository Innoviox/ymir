import numpy as np
from visualizer.sprite.util import *
from abc import ABC, abstractmethod
from collections import defaultdict
from .animator import Animator
from .tile import Tile

GRAVITY = -.5

class Sprite(Tile, ABC):
    def __init__(self, position, typ, controller, **kwargs):
        self.gravity = kwargs.pop("gravity", True)

        super().__init__(position, typ, controller, **kwargs, z_index=2)

        self.can_jump = True
        self.position = np.array(position, dtype = 'float64')
        self.velocity = np.array([0, 0], dtype='float64')
        self.friction = 0.1  # value between 0 and 1; larger means more friction
        self.horizontal_speed = 10.0
        self.jump_speed = 2.0
        self.on_moving_tile = False
        self.dead = False

    def update_render(self):
        self.entity.x = self.position[0]
        self.entity.y = self.position[1]
        self.entity.z = -1 # render on top of everything else

    def update_collisions(self, tiles, tile_array):
        collided = defaultdict(list)

        if len(tiles) == 0:
            pass
        elif len(tiles) == 2:
            # vertically stacked tiles, snap horizontally
            t = tiles[0]
            if tiles[0].x == tiles[1].x:
                collided[collide(self, t, x=True)].append(t)
            else: # horizontally connected tiles, snap vertically
                collided[collide(self, tiles[0], x=False)].append(t)
        else:
            # position snapping, only if a single tile is collided, this will be buggy
            for tile in tiles:
                try:
                    v = self.velocity[0]
                    if self.on_moving_tile:
                        v = self.on_moving_tile.speed * 10
                    horiz_time = min(abs(self.position[0] - tile.x - 1.0)
                                    , abs(self.position[0] + 1.0 - tile.x)) / abs(v)
                except:
                    horiz_time = 1000
                try:
                    vert_time = min(abs(self.position[1] - tile.y - 1.0)
                                    , abs(self.position[1] + 1.0 - tile.y)) / abs(self.velocity[1])
                except:
                    vert_time = 1000
                # print(tiles, self.position, tile.position, self.velocity, vert_time, horiz_time)
                if vert_time == horiz_time:
                    collided[collide(self, tile, x=False)].append(tile)
                    collided[collide(self, tile, x=True)].append(tile)
                elif vert_time < horiz_time:
                    # vertical position snapping
                    collided[collide(self, tile, x=False)].append(tile)
                else:
                    # horizontal position snapping
                    collided[collide(self, tile, x=True)].append(tile)
        return collided

    #abstract please overwrite me
    @abstractmethod
    def update(self, dt):
        self.update_position_velocity(dt)
        self.update_render()
        if self.animator:
            self.animator.update()

    def update_position_velocity(self, dt):
        self.on_moving_tile = False
        self.position += self.velocity * dt
        self.velocity[0] += -self.velocity[0] * (1-self.friction) * dt # slow down due to friction
        if self.gravity:
            self.velocity[1] += GRAVITY * dt

    def collide(self, tile, direction):
        return False

    def die(self):
        self.controller.sprites.remove(self)
        self.dead = True