from enum import Enum

class TileType(Enum):
    GROUND = 1
    AIR = 2
    START = 3
    END = 4

class Tile():
    def __init__(self,position, image, type):
        self.position = position
        self.image = image
        self.type = type