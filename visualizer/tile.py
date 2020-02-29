'''
Create a 'Tile' object with type and (x,y) location. 
'''
from enum import Enum
from ursina import *

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
    "grassHalf"
]

tile_map = 'AOSEseWawM'

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

    def texture(self):
        return texture_map[self.value - 1]

    @classmethod
    def from_tile(cls, t):
        return cls._value2member_map_[tile_map.index(t) + 1]

    # todo: make better
    def is_ground(self): return self.value in [1, 8]
    def is_water(self): return self.value in [7, 9]

class Tile():
    def __init__(self, position, typ):
        self.position = position
        self.type = typ
        self.texture = self.type.texture()
        self.entity = None

    def update(self, tiles): pass

    @property
    def x(self):
        return self.position[0]

    def __repr__(self):
        return str(self.type) + " at " + str(self.position)

    @property
    def y(self):
        return self.position[1]

class HorizontalMovingTile(Tile):
    def __init__(self, position, typ):
        super().__init__(position, typ)
        self.cycle_length = 50
        self.curr = 0
        self.speed = 0.1

    def update(self, tiles):
        super().update(tiles)

        self.entity.x += self.speed

        px, py = int(self.entity.x), int(self.entity.y)

        if tiles[py][px + bool(self.speed > 0)].type.is_ground(): # todo: moving platforms can't collide with other moving platforms
            self.speed = -self.speed

