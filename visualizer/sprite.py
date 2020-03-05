import numpy as np
from visualizer.util import *
from abc import ABC, abstractmethod

class Sprite(ABC):
    def __init__(self, position, entity):
        self.can_jump = True
        self.position = np.array(position,dtype = 'float64')
        self.entity = entity
        self.velocity = np.array([0, 0], dtype='float64')
        self.friction = 0.1# value between 0 and 1; larger means more friction
        self.horizontal_speed = 10.0
        self.jump_speed = 2.0
        self.on_moving_tile = False

    def update_render(self):
        self.entity.x = self.position[0]
        self.entity.y = self.position[1]
        self.entity.z = -1 # render on top of everything else

    def update_collisions(self, tiles, tile_array):

        if len(tiles) == 0:
            return

        if len(tiles) == 2:
            tile = tiles[0]
            # vertically stacked tiles, snap horizontally
            chg = True
            if tiles[0].x == tiles[1].x:
                chg = collide(self, tiles[0], x=True)
            else: # horizantally connected tiles, snap vertically
                chg = collide(self, tiles[0], x=False)
            if chg:
                yield tile

        else:
            tile = tiles[0]
            # position snapping, only if a single tile is collided, this will be buggy

            try:
                horiz_time = min(abs(self.position[0] - tile.x - control.scale)
                                , abs(self.position[0] + control.scale - tile.x)) / abs(self.velocity[0])
            except:
                horiz_time = 1000
            try:
                vert_time = min(abs(self.position[1] - tile.y - control.scale)
                                , abs(self.position[1] + control.scale - tile.y)) / abs(self.velocity[1])
            except:
                vert_time = 1000
            chg = True
            if vert_time == horiz_time:
                chg = collide(self, tile, x=False)
                chg = collide(self, tile, x=True)
            elif vert_time < horiz_time:
                # vertical position snapping
                chg = collide(self, tile, x=False)
            else:
                # horizontal position snapping
                chg = collide(self, tile, x=True)
            if chg:
                yield tile

    #abstract please overwrite me
    @abstractmethod
    def update(self,dt):
        self.update_position_velocity(dt)
        self.update_render()

    def update_position_velocity(self, dt):
        self.on_moving_tile = False
        self.position += self.velocity * dt
        self.velocity[0] += -self.velocity[0] * (1-self.friction) * dt # slow down due to friction
        self.velocity[1] += control.gravity * dt
