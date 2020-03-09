import numpy as np
from visualizer.util import *
from abc import ABC, abstractmethod
from collections import defaultdict
from ursina import load_texture

class Sprite(ABC):
    def __init__(self, position, entity, controller, gravity=True, anim_texture=None):
        self.can_jump = True
        self.position = np.array(position,dtype = 'float64')
        self.entity = entity
        self.controller = controller
        self.velocity = np.array([0, 0], dtype='float64')
        self.friction = 0.1# value between 0 and 1; larger means more friction
        self.horizontal_speed = 10.0
        self.jump_speed = 2.0
        self.on_moving_tile = False

        self.animator = Animator(self, anim_texture) if anim_texture else None
        self.gravity = gravity

        self._hitbox = [0, 0, 1, 1]
        self.hitbox = None
        self.dead = False

    def update_render(self):
        self.entity.x = self.position[0]
        self.entity.y = self.position[1]
        self.entity.z = -1 # render on top of everything else

    def update_collisions(self, tiles, tile_array):
        collided = defaultdict(list)

        if len(tiles) == 0:
            pass
        elif len(tiles) == 2:
            # vertically stacked tiles, snap horizontally
            t = tiles[0]
            if tiles[0].x == tiles[1].x:
                collided[collide(self, t, x=True)].append(t)
            else: # horizontally connected tiles, snap vertically
                collided[collide(self, tiles[0], x=False)].append(t)
        else:
            # position snapping, only if a single tile is collided, this will be buggy
            for tile in tiles:
                try:
                    v = self.velocity[0]
                    if self.on_moving_tile:
                        v = self.on_moving_tile.speed * 10
                    horiz_time = min(abs(self.position[0] - tile.x - control.scale)
                                    , abs(self.position[0] + control.scale - tile.x)) / abs(v)
                except:
                    horiz_time = 1000
                try:
                    vert_time = min(abs(self.position[1] - tile.y - control.scale)
                                    , abs(self.position[1] + control.scale - tile.y)) / abs(self.velocity[1])
                except:
                    vert_time = 1000
                # print(tiles, self.position, tile.position, self.velocity, vert_time, horiz_time)
                if vert_time == horiz_time:
                    collided[collide(self, tile, x=False)].append(tile)
                    collided[collide(self, tile, x=True)].append(tile)
                elif vert_time < horiz_time:
                    # vertical position snapping
                    collided[collide(self, tile, x=False)].append(tile)
                else:
                    # horizontal position snapping
                    collided[collide(self, tile, x=True)].append(tile)
        return collided

    #abstract please overwrite me
    @abstractmethod
    def update(self,dt):
        self.update_position_velocity(dt)
        self.update_render()
        if self.animator:
            self.animator.update()

    def update_position_velocity(self, dt):
        self.on_moving_tile = False
        self.position += self.velocity * dt
        self.velocity[0] += -self.velocity[0] * (1-self.friction) * dt # slow down due to friction
        if self.gravity:
            self.velocity[1] += control.gravity * dt

    def set_animator(self, texture):
        self.animator = Animator(self, texture)
        self.animator.start()

    @property
    def x(self):
        return self.entity.x

    @property
    def y(self):
        return self.entity.y

    def collide(self, tile, direction):
        return False

    def die(self):
        self.dead = True

class Animator:
    def __init__(self, sprite, base_texture, anim_every=10, cycle=True):
        self.sprite = sprite
        self.anim_every = anim_every
        self.anim_step = 0
        self.anim_frame = 1
        self.base_texture = base_texture
        self.animating = True
        self.anim_dir = 1
        self.cycle = cycle

        self.max_frames = 1
        while load_texture(f"{self.base_texture}_{self.max_frames + 1}"):
            self.max_frames += 1

    def update(self):
        if self.animating:
            self.anim_step += 1
            if self.anim_step % self.anim_every == 0:
                self.animate()

    def animate(self):
        self.sprite.entity.texture = f"{self.base_texture}_{self.anim_frame}"

        if self.cycle:
            if self.anim_frame == self.max_frames:
                self.anim_dir = -1
            elif self.anim_frame == 1:
                self.anim_dir = 1
        else:
            if self.anim_frame == self.max_frames:
                self.anim_frame = 1

        self.anim_frame += self.anim_dir

    def start(self):
        self.animating = True

    def stop(self):
        self.animating = False

    def kill(self):
        self.stop()
        self.sprite.entity.texture = f"{self.base_texture}_dead"