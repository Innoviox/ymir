'''
Create a 'Tile' object with type and (x,y) location. 
'''
from .util import *
from .animator import Animator


class Tile():
    def __init__(self, position, typ, controller, hitbox=HITBOX): # hitbox: min-x, min-y, max-x, max-y
        self.position = position
        self.hitbox = Hitbox(hitbox[:])

        self.type = typ
        self.texture = self.type.texture()
        self.entity = None
        self.controller = controller
        self.animator = Animator(self, self.texture)

    def load(self, new_type, texture=True):
        self.type = new_type
        self.texture = self.type.texture()
        if self.entity and texture:
            self.entity.texture = self.texture

    def load_toggle(self): self.load(self.type.toggle())

    def update(self, dt):
        ...

    def collide(self, tile, direction):
        return True  # if this method is called, then self.type.collides()

    @property
    def x(self):
        return self.position[0]
    @property
    def y(self):
        return self.position[1]

    def __repr__(self):
        return str(self.type).split(".")[1]# + " at " + str(self.position)

    def hide(self, now=False):
        self.type = TileType.AIR
        if now:
            self.entity.hide()
        else:
            self.entity.fade_out()

    def setup(self):
        ...