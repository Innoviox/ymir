'''
Create a 'Player' object that stores all of the necessary physics-y info
(and rendering crap). Also the animation state, eventually?
'''
import numpy as np
from visualizer.util import *

class Player():
    def __init__(self, position, entity):
        self.position = position
        self.entity = entity
        self.input = [0,0]
        self.velocity = np.array([0,0],dtype='float64')
        self.friction = 0.1 # value between 0 and 1; larger means more friction

    def update_render(self):
        self.entity.x = self.position[0]
        self.entity.y = self.position[1]
        self.entity.z = -1 # render on top of everything else
        
    def update_position_velocity(self, dt):
        self.position += self.velocity * dt
        self.velocity += -self.velocity * (1-self.friction) * dt 
        self.velocity += self.input
