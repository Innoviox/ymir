from ursina import *
from ursina.input_handler import held_keys
from Util import *
import numpy as np

class Controller():
    speed_cap = 2
    dt = .1
    def __init__(self, player):
        self.player = player
        self.app = Ursina()

    def process_input(self):
        self.player.input = self.dt * np.array([held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']])
        print(self.player.input)
    def update(self):
        self.process_input()
        self.player.position += self.player.velocity
        self.player.velocity += -self.player.velocity / self.speed_cap
        if mag(self.player.velocity + self.player.input) < self.speed_cap:
            self.player.velocity += self.player.input



        self.player.update()

    def start(self):
        self.app.run()