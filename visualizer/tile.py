'''
Create a 'Tile' object with type and (x,y) location. 
'''
from enum import Enum
from ursina import *

from visualizer import util
from visualizer.util import *

TEXTURES = {
    'A': 'grassCenter',
    'O': None,
    'S': 'door_openMid',
    's': 'door_closedMid',
    'E': 'door_openTop',
    'e': 'door_closedTop',
    'W': 'liquidWater',
    'a': 'grassMid',
    'w': 'liquidWaterTop_mid',
    'M': 'grassHalfMid',
    'c': 'flagPole',
    'C': 'flagGreen_up',
    'P': 'spikes',
    'N': 'grassHalfLeft',
    ',': 'grassHalfRight'
}

texture_map = list(TEXTURES.values())
tile_map = ''.join(TEXTURES.keys())

class TileType(Enum):
    GROUND = 1
    AIR = 2
    START = 3
    END = 4
    START_TOP = 5
    END_TOP = 6
    WATER = 7
    GROUND_TOP = 8
    WATER_TOP = 9
    MOVING = 10
    CHECKPOINT = 11
    CHECKPOINT_ON = 12
    SPIKES = 13
    MOVING_LEFT = 14
    MOVING_RIGHT = 15

    def texture(self):
        return texture_map[self.value - 1]

    @classmethod
    def from_tile(cls, t):
        return cls._value2member_map_[tile_map.index(t) + 1]

    # todo: make better
    def is_ground(self): return self.value in [1, 8]
    def is_water(self): return self.value in [7, 9]
    def collides(self):
        return self.is_ground() or self.value in [13]
    def deadly(self):
        return self.value in [13]


    def toggle(self):
        return TileType.from_tile(tile_map[self.value - 1].swapcase())

class Hitbox():
    def __init__(self, hb):
        self._hb = hb[:]

    @property
    def min_x(self): return self._hb[0]

    @property
    def min_y(self): return self._hb[1]

    @property
    def max_x(self): return self._hb[2]

    @property
    def max_y(self): return self._hb[3]
HITBOX=[0.0, 0.0, 1.0, 1.0]

class Tile():
    def __init__(self, position, typ, controller, hitbox=HITBOX): # hitbox: min-x, min-y, max-x, max-y
        self.position = position
        self.hitbox = Hitbox(hitbox[:])

        self.type = typ
        self.texture = self.type.texture()
        self.entity = None
        self.controller = controller

    def load(self, new_type):
        self.type = new_type
        self.texture = self.type.texture()
        if self.entity:
            self.entity.texture = self.texture

    def update(self): pass

    @property
    def x(self):
        return self.position[0]

    def __repr__(self):
        return str(self.type) + " at " + str(self.position)

    @property
    def y(self):
        return self.position[1]

def HitboxTile(hitbox):
    class _T(Tile):
        def __init__(self, *args):
            super().__init__(*args, hitbox=hitbox)

    return _T

class HorizontalMovingTile(Tile):
    def __init__(self, *args):
        super().__init__(*args, hitbox=[0.0, 0.5, 1.0, 1.0])

        self.speed = 0.1
        self.offset = [0, 1]

    def update(self):
        super().update()

        for entity in self.controller.sprites:
            if not entity.on_moving_tile and util.inside(entity.position + [0,-.1], self):
                entity.position[0] += self.speed
                entity.on_moving_tile = True # todo: fix jolting?

        self.entity.x += self.speed
        self.position[0] += self.speed

        px, py = int(self.entity.x), int(self.entity.y)

        if self.controller.tile_array[py][px + self.offset[self.speed > 0]].type.is_ground():
            self.speed = -self.speed

    def set_offset(self, offset, total):
        if total == 1:
            return

        self.load(TileType.from_tile(f"N{'M' * (total - 2)},"[offset]))
        self.offset = [-offset, total - offset]

class CheckpointTile(Tile):
    def update(self):
        super().update()

        if self.type == TileType.CHECKPOINT:
            if int(self.controller.player.entity.x) == int(self.entity.x) and int(self.controller.player.entity.y) == int(self.entity.y):
                self.load(self.type.toggle())
                self.controller.starting_tile = self

spikes_hitboxes = [
    [0.1, 0, 0.9, 0.25],
    [0.1, 0.75, 0.9, 1],
    [0.85, 0.1, 1, 0.9],
    [0, 0.1, 0.15, 0.9]
]

class SpikesTile(Tile):
    def __init__(self, *args):
        super().__init__(*args)

    def set_direction(self):
        l = len(self.controller.tile_array)
        for (hb, (dx, dy), rot) in zip(spikes_hitboxes,
                                  [[0, -1], [0, 1], [1, 0], [-1, 0]],
                                   [0, 180, 270, 90]):
            nx, ny = self.position[0] + dx, l - (self.position[1] + dy) - 1
            if 0 <= ny < l and \
                0 <= nx < len(self.controller.tile_array[ny]) and \
                self.controller.tile_array[ny][nx].type.is_ground():
                self.hitbox = Hitbox(hb)
                self.entity.rotation_z = rot
                return


tile_classes = {'M': HorizontalMovingTile, 'c': CheckpointTile, 'P': SpikesTile}