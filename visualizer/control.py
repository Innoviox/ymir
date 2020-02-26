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

class Controller():
    dt = .1
    scale = 1

    def __init__(self):
        self.app = Ursina()
        self.entities = []

        camera.orthographic = True
        camera.fov = 25

        window.fullscreen = True

    def process_input(self):
        self.player.input = self.dt * np.array([held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']])

    def update(self):
        self.process_input()
        self.player.update_position_velocity(self.dt)
        self.player.update_render()

    def build_from_array(self, array):
        for y,row in enumerate(array):
            for x,tile in enumerate(row):
                self.entities.append(Entity(model="cube", 
                    texture=tile.texture,
                    scale = self.scale,
                    position=(self.scale*tile.x,self.scale*tile.y,0)))

    def start(self):
        load_ground_textures()
        reader = FileReader("visualizer/test_file.txt")
        self.build_from_array(reader.read())
        self.player = Player(np.array([0,0],dtype='float64'),
	Entity(model="cube",color=color.blue,scale=1))
        input_handler.bind('right arrow', 'd')
        input_handler.bind('left arrow', 'a')
        input_handler.bind('up arrow', 'w')
        input_handler.bind('down arrow', 's')
        self.app.run()