'''
Create a 'Player' object that stores all of the necessary physics-y info
(and rendering crap). Also the animation state, eventually?
'''
import numpy as np
from visualizer.util import *
from math import sqrt

#TODO get crushed
class Player():
    def __init__(self, position, entity):
        self.can_jump = True
        self.position = position
        self.entity = entity
        self.input = [0, 0]
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
            if tiles[0].x == tiles[1].x:
                if tile.x < self.position[0] < tile.x + control.scale:
                    self.position[0] = tile.x + control.scale
                elif tile.x < self.position[0] + control.scale < tile.x + control.scale:
                    self.position[0] = tile.x - control.scale
                self.velocity[0] = 0
            else: # horizantally connected tiles, snap vertically
                if tile.y < self.position[1] < tile.y + control.scale:
                    self.position[1] = tile.y + control.scale
                    self.can_jump = True
                elif tile.y < self.position[1] + control.scale < tile.y + control.scale:
                    self.position[1] = tile.y - control.scale
                self.velocity[1] = 0


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
            if vert_time == horiz_time:
                if tile.y < self.position[1] < tile.y + control.scale:
                    self.position[1] = tile.y + control.scale
                    self.velocity[1] = 0
                    #hit the ground
                    self.can_jump = True
                elif tile.y < self.position[1] + control.scale < tile.y + control.scale:
                    self.position[1] = tile.y - control.scale
                    self.velocity[1] = 0

                if tile.x < self.position[0] < tile.x + control.scale:
                    self.position[0] = tile.x + control.scale
                    self.velocity[0] = 0
                elif tile.x < self.position[0] + control.scale < tile.x + control.scale:
                    self.position[0] = tile.x - control.scale
                    self.velocity[0] = 0
            elif vert_time < horiz_time:
                # vertical position snapping
                if tile.y < self.position[1] < tile.y + control.scale:
                    self.position[1] = tile.y + control.scale
                    self.velocity[1] = 0
                    #hit the ground
                    self.can_jump = True
                elif tile.y < self.position[1] + control.scale < tile.y + control.scale:
                    self.position[1] = tile.y - control.scale
                    self.velocity[1] = 0
            else:
                # horizontal position snapping
                if tile.x < self.position[0] < tile.x + control.scale:
                    self.position[0] = tile.x + control.scale
                    self.velocity[0] = 0
                elif tile.x < self.position[0] + control.scale < tile.x + control.scale:
                    self.position[0] = tile.x - control.scale
                    self.velocity[0] = 0

    def update_position_velocity(self, dt):
        self.on_moving_tile = False
        self.position += self.velocity * dt
        self.velocity[0] += self.input[0] * self.horizontal_speed * dt # slow down due to friction
        self.velocity[0] += -self.velocity[0] * (1-self.friction) * dt # slow down due to friction
        self.velocity[1] += control.gravity * dt
        # print("velocity:", self.velocity, "input:", self.input, "position:", self.position)

        if self.can_jump and self.input[1] > 0:
            self.velocity[1] += self.jump_speed
            self.can_jump = False
        else:
            if self.input[1] > 0:
                self.input[1] = 0
