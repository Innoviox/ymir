'''
Create a 'Player' object that stores all of the necessary physics-y info
(and rendering crap). Also the animation state, eventually?
'''
import numpy as np
from visualizer.util import *
from math import sqrt

class Player():
    def __init__(self, position, model):
        self.can_jump = True
        self.position = position
        self.model = model
        self.input = [0, 0]
        self.velocity = np.array([0, 0], dtype='float64')
        self.speed_cap = 10

    def update_render(self):
        self.model.x = self.position[0]
        self.model.y = self.position[1]
        self.model.z = -1

    def update_collisions(self, tiles, tile_array):

        if len(tiles) == 0:
            return

        if len(tiles) == 2:
            tile = tiles[0]
            #vertically stacked tiles, snap horizantlly
            if tiles[0].x == tiles[1].x:
                if tile.x < self.position[0] < tile.x + control.scale:
                    self.position[0] = tile.x + control.scale
                elif tile.x < self.position[0] + control.scale < tile.x + control.scale:
                    self.position[0] = tile.x - control.scale
                self.velocity[0] = 0
            else: #horizantally connected tiles, snap vertically
                if tile.y < self.position[1] < tile.y + control.scale:
                    self.position[1] = tile.y + control.scale
                    self.can_jump = True
                elif tile.y < self.position[1] + control.scale < tile.y + control.scale:
                    self.position[1] = tile.y - control.scale
                self.velocity[1] = 0

        elif len(tiles) == 3: #snap player to the "missing" tile
            missing_tile = list(filter(lambda x: not x in tiles, get_nearby_tiles(self.position,tile_array)))[0]
            self.position=missing_tile.position
            self.velocity = np.array([0, 0], dtype='float64')

        else:
            #position snapping, only if a single tile is collided, this will be Buggy
            tile = tiles[0]
            #vertical position snapping
            if tile.y < self.position[1] < tile.y + control.scale:
                self.position[1] = tile.y + control.scale
                self.velocity[1] = 0
                self.can_jump = True
            elif tile.y < self.position[1] + control.scale < tile.y + control.scale:
                self.position[1] = tile.y - control.scale
                self.velocity[1] = 0

            #horizontal position snapping
            if tile.x < self.position[0] < tile.x + control.scale:
                self.position[0] = tile.x + control.scale
                self.velocity[0] = 0
            elif tile.x < self.position[0] + control.scale < tile.x + control.scale:
                self.position[0] = tile.x - control.scale
                self.velocity[0] = 0

    def update_position_velocity(self, dt):
        self.position += self.velocity * dt
        self.velocity += -self.velocity / self.speed_cap * dt * 3
        self.velocity[1] += control.gravity * dt

        if self.can_jump and self.input[1] > 0:
            self.input[1] = self.speed_cap/3
            self.velocity[1] += self.input[1]
            self.can_jump = False
        else:
            if self.input[1] > 0:
                self.input[1] = 0

        if self.velocity[0] + self.input[0] < self.speed_cap:
            self.velocity[0] += self.input[0]