'''
Create a 'Player' object that stores all of the necessary physics-y info
(and rendering crap). Also the animation state, eventually?
'''
import numpy as np
from visualizer.util import *

class Player():
    def __init__(self, position, model):
        self.position = position
        self.model = model
        self.input = [0,0]
        self.velocity = np.array([0,0],dtype='float64')
        self.speed_cap = 10

    def update_render(self):
        self.model.x = self.position[0]
        self.model.y = self.position[1]
        self.model.z = -1
        
    def update_position_velocity(self, dt):
        self.position += self.velocity * dt
        self.velocity += -self.velocity / self.speed_cap * dt * 10
        if mag(self.velocity + self.input) < self.speed_cap:
            self.velocity += self.input
