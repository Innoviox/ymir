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
camera_fov = 20
camera_offset = [0,1,-30]
camera_speed = 2
gravity = -.5

h, w = window.size
OFFSET_X = 0
OFFSET_Y = 0
del h, w

class Controller():
    def __init__(self):
        self.app = Ursina()
        self.entities = []
        self.tile_array = []
        camera.orthographic = True
        camera.fov = camera_fov
        window.borderless = False 

        # window.fullscreen = True

    def process_input(self):
        self.player.input = dt * np.array([held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']])

    def update(self):
        self.process_input()
        self.player.update_position_velocity(dt)
        self.player.update_render()
        self.player.update_collisions(self.player_colliding(),self.tile_array)

    #returns the ground tiles collided with, or an empty list for no collisions
    def player_colliding(self):
        collided_tiles = list(filter(lambda x: inside(self.player.position, x), get_nearby_ground_tiles(self.player.position, self.tile_array)))
        return collided_tiles

    def build_from_array(self, array):
        self.tile_array = array
        for y, row in enumerate(array):
            for x, tile in enumerate(row):
                if tile.texture is None: continue
                self.entities.append(Entity(model="cube",
                                            texture=tile.texture,
                                            scale=scale,
                                            position=(round(OFFSET_X + scale * tile.x),
                                                      round(OFFSET_Y + scale * tile.y), 0)))
                if tile.type == TileType.START:
                    self.starting_tile = tile
                if tile.type == TileType.END:
                    self.ending_tile = tile


    def load_level(self, level_file_name):
        reader = FileReader(level_file_name)
        self.build_from_array(reader.read())
        print(self.starting_tile.position)
        self.player.position = np.add(np.array(self.starting_tile.position, dtype='float64'), [0,2])
        print(self.player.position)

    def start(self):
        self.player = Player(position=np.array([0,2], dtype='float64'),
                             entity=Entity(model="cube", color=color.blue, scale=1))
        camera.parent = self.player.entity
        camera.add_script(SmoothFollow(target=self.player.entity, offset=camera_offset, speed=camera_speed))
        input_handler.bind('right arrow', 'd')
        input_handler.bind('left arrow', 'a')
        input_handler.bind('up arrow', 'w')
        input_handler.bind('down arrow', 's')
        self.load_level("visualizer/test_file.txt")
        self.app.run()