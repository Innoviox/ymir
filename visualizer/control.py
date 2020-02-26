'''
Central hub of the code, basically. Calls the necessary functions to 
render the scene, get input, move the player, etc. 
'''
from ursina import *
from ursina.input_handler import held_keys

from visualizer.player import Player
from visualizer.util import *
import numpy as np
from visualizer.assets import *
from visualizer.FileReader import *

scale = 1
dt = .1

h, w = window.size
OFFSET_X = -15
OFFSET_Y = -10
del h, w

class Controller():
    def __init__(self):
        self.app = Ursina()
        self.entities = []
        self.tile_array = []
        camera.orthographic = True
        camera.fov = 25

        # window.fullscreen = True

    def process_input(self):
        self.player.input = dt * np.array([held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']])

    def update(self):
        self.process_input()
        self.player.update_position_velocity(dt)
        self.player.update_render()
        print(self.player_colliding())

    #returns the ground tiles collided with, or an empty list for no collisions
    def player_colliding(self):
        collided_tiles = list(filter(lambda x: inside(self.player, x), get_nearby_ground_tiles(self.player.position, self.tile_array)))
        return collided_tiles

    def build_from_array(self, array):
        self.tile_array = array
        for y, row in enumerate(array):
            for x, tile in enumerate(row):
                if tile.texture is None: continue
                self.entities.append(Entity(model="cube",
                                            texture=tile.texture,
                                            scale=scale,
                                            position=(OFFSET_X + scale * tile.x, OFFSET_Y + scale * tile.y, 0)))
                if tile.type == TileType.START:
                    self.starting_tile = tile
                if tile.type == TileType.END:
                    self.ending_tile = tile

    def start(self):
        reader = FileReader("visualizer/test_file.txt")
        self.build_from_array(reader.read())
        self.player = Player(np.array(self.starting_tile.position, dtype='float64'),
                             Entity(model="cube", color=color.blue, scale=1))
        input_handler.bind('right arrow', 'd')
        input_handler.bind('left arrow', 'a')
        input_handler.bind('up arrow', 'w')
        input_handler.bind('down arrow', 's')
        self.app.run()