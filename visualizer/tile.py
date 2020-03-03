'''
Create a 'Tile' object with type and (x,y) location. 
'''
from enum import Enum
from ursina import *

from visualizer import util
from visualizer.util import *
texture_map = [
    "grassCenter",
    None,
    "door_openMid",
    "door_closedMid",
    "door_openTop",
    "door_closedTop",
    "liquidWater",
    "grassMid",
    "liquidWaterTop_mid",
    "grassHalfMid",
    "flagPole",
    "flagGreen_up",
    "spikes",
    "grassHalfLeft",
    "grassHalfRight"
]

tile_map = 'AOSEseWawMcCPN,'

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

    def toggle(self):
        return TileType.from_tile(tile_map[self.value - 1].swapcase())

class Tile():
    def __init__(self, position, typ, controller, hitbox = []):
        self.position = position
        self.hitbox = hitbox

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

class HorizontalMovingTile(Tile):
    def __init__(self, position, typ, controller):
        super().__init__(position, typ, controller)
        self.speed = 0.1
        self.offset = [0, 1]

    def update(self):
        super().update()

        if not self.controller.player.on_moving_tile and util.inside(self.controller.player.position + [0,-.1], self):
            self.controller.player.position[0] += self.speed
            self.controller.player.on_moving_tile = True

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
    def __init__(self, position, typ, c):
        super().__init__(position, typ, c)

    def update(self):
        super().update()

        if self.type == TileType.CHECKPOINT:
            if int(self.controller.player.entity.x) == int(self.entity.x) and int(self.controller.player.entity.y) == int(self.entity.y):
                self.load(self.type.toggle())
                self.controller.starting_tile = self

tile_classes = {'M': HorizontalMovingTile, 'c': CheckpointTile}