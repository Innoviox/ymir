import numpy as np

class Player():
    def __init__(self, position, model):
        self.position = position
        self.model = model
        self.input = [0,0]
        self.velocity = np.array([0,0],dtype='float64')

    def update(self):
        self.model.x = self.position[0]
        self.model.y = self.position[1]