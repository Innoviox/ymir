import numpy as np

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

    def update_position_velocity(self, dt):
        self.position += self.velocity * dt
        self.velocity += -self.velocity / self.speed_cap * dt
        if mag(self.velocity + self.input) < self.speed_cap:
            self.velocity += self.input
