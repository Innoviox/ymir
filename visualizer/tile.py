'''
Create a 'Tile' object with type and (x,y) location. 
'''
from enum import Enum
from ursina import *

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

    def texture(self):
        return [
            "grassCenter",
            None,
            "door_openMid",
            "door_closedMid",
            "door_openTop",
            "door_closedTop",
            "liquidWater",
            "grassMid",
            "liquidWaterTop_mid"
        ][self.value - 1]

    def is_ground(self): return self.value in [1, 8]
    def is_water(self): return self.value in [7, 9]

class Tile():
    def __init__(self, position, typ):
        self.position = position
        self.texture = typ.texture()
        self.type = typ

    @property
    def x(self):
        return self.position[0]

    def __repr__(self):
        return str(self.type) + " at " + str(self.position)

    @property
    def y(self):
        return self.position[1]