from ursina import *
from ursina.input_handler import held_keys
from visualizer.util import *
import numpy as np
from visualizer.assets import *
from visualizer.FileReader import *

class Controller():
    speed_cap = 2
    dt = .1
    scale = .4

    def __init__(self, player):
        self.player = player
        self.app = Ursina()
        self.entities = []

    def process_input(self):
        self.player.input = self.dt * np.array([held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']])

    def update(self):
        self.process_input()
        self.player.position += self.player.velocity
        self.player.velocity += -self.player.velocity / self.speed_cap
        if mag(self.player.velocity + self.player.input) < self.speed_cap:
            self.player.velocity += self.player.input
        self.player.update()

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
        self.app.run()