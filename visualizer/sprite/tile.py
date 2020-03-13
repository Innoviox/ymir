'''
Create a 'Tile' object with type and (x,y) location. 
'''
from .util import *
from .animator import Animator
from ursina import Entity
from visualizer.constants import TileType

class Tile():
    def __init__(self, position, typ, controller, hitbox=[0.0, 0.0, 1.0, 1.0], z_index=2): # hitbox: min-x, min-y, max-x, max-y
        self.position = position
        self.hitbox = Hitbox(hitbox[:])
        self.type = typ
        self.texture = self.type.default_texture()
        self.entity = None
        self.controller = controller
        self.animator = Animator(self, self.texture)
        self.z_index = z_index

        if self.texture:
            self.make_entity()

    def make_entity(self):
        self.entity = Entity(model="quad",
                             texture=self.texture,
                             scale=1,
                             position=(round(self.x),
                                       round(self.y), self.z_index))

    def load(self, new_type, texture=True):
        """Change the type of the tile to new_type. 
        If texture is True, then also change the texture."""
        self.type = new_type
        self.texture = self.type.default_texture()
        if self.entity and texture:
            self.entity.texture = self.texture

    def load_toggle(self):
        self.load(self.type.toggle())

    def update(self, dt):
        ...

    def collide(self, tile, direction, commit=True):
        return True  # if this method is called, then self.type.collides()

    @property
    def x(self):
        return self.position[0]
    @property
    def y(self):
        return self.position[1]

    def __repr__(self):
        return str(self.type).split(".")[1] + f" at {self.position}"

    def hide(self, now=False):
        self.type = TileType.AIR
        if now:
            self.entity.hide()
        else:
            self.entity.fade_out()

    def setup(self):
        ...

    def inside(self, tile, density=10):  # TODO: transparency (hitboxes)
        """Tells if this tile is inside the given tile.
        Works by testing the boundary points of the one by one box with the bottom left corner
        in the specified position."""
        return self.inside_position(tile.position, tile.hitbox, density=density)

    def inside_position(self, position, hitbox, density=10):
        for i in range(density):
            if point_inside([self.position[0] + i / density * (self.hitbox.max_x - self.hitbox.min_x), self.position[1] + self.hitbox.min_y],
                            position, hitbox):
                return True
            if point_inside([self.position[0] + i / density * (self.hitbox.max_x - self.hitbox.min_x), self.position[1] + self.hitbox.max_y],
                            position, hitbox):
                return True
            if point_inside([self.position[0] + self.hitbox.min_x, self.position[1] + i / density * (self.hitbox.max_y - self.hitbox.min_y)],
                            position, hitbox):
                return True
            if point_inside([self.position[0] + self.hitbox.max_x, self.position[1] + i / density * (self.hitbox.max_y - self.hitbox.min_y)],
                            position, hitbox):
                return True
        return False