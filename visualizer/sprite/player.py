'''
Create a 'Player' object that stores all of the necessary physics-y info
(and rendering crap). Also the animation state, eventually?
'''
import numpy as np

from .sprite import Sprite
from ursina.input_handler import held_keys

class Player(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, z_index=4)
        self.animator.stop()
        self.animator.anim_every = 5
        self.animator.cycle = False

    def setup(self):
        self.entity.double_sided = True

    def update(self, dt):
        self.process_input(dt)
        super().update(dt)

    def process_input(self,dt):
        """Get player keyboard (WASD) held keys, store in player.input."""
        self.input = dt * np.array([held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']])

    def update_position_velocity(self, dt):
        """Update position and velocity."""
        super().update_position_velocity(dt)
        # move horizontally based on player input
        self.velocity[0] += self.input[0] * self.horizontal_speed * dt 

        if self.input[1] > 0: # player trying to move upwards
            if self.can_jump: # jump if able
               self.jump()
            else: # if you can't jump, then null player input upwards
                self.input[1] = 0

        if self.velocity[0] < 0: # can't rotate player because then the camera would rotate
            self.animator.set_base("_flipped")
        elif self.velocity[0] > 0:
            self.animator.set_base("")

        if self.velocity[1] > 0.1:
            self.animator.set_texture("jump")
        elif self.velocity[1] < -0.1:
            self.animator.set_texture("fall")
        elif abs(self.velocity[0]) > 0.2:
            self.animator.start()
        else:
            self.animator.stop()

    def jump(self):
        self.velocity[1] += self.jump_speed
        self.can_jump = False

    def die(self):
        self.controller.die()