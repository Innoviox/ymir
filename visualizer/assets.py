'''
Get asset files from the disk, turn them into actually useful Ursina entities.
Also, enums.
'''
from enum   import Enum
from random import choice
from ursina import load_texture, compress_textures
from shutil import copyfile
from visualizer.tile import TileType
from functools import lru_cache

class GroundType(Enum):
    BOTTOM = 0
    TOP = 1
    LEFT = 2
    RIGHT = 3
    NONE = 4

    def file_name(self, typ):
        if typ == "Ground":
            return ["Center", "Mid", "Left", "Right"][self.value]
        elif typ == "Water":
            return ["", "Top_mid"][self.value]


class Theme(Enum):
    CASTLE, DIRT, GRASS, SAND, SNOW, STONE = range(6)

def load_ground_textures():
    # DON'T CALL THIS METHOD
    return
    # for theme in Theme:
    #     for typ in GroundType:
    #         file = f"visualizer/assets/tiles/{theme.name.lower()}/{typ.name.lower()}.png"
    #         name = f"visualizer/textures/{theme.name.lower()}_{typ.name.lower()}.png"
    #         copyfile(file, name)
    #         # print(load_texture(name, file))

@lru_cache(maxsize=None)
def _load_texture(file):
    load_texture(file, "visualizer/"+file)
    return file

def texture(c: TileType, typ: GroundType, theme: Theme=None) -> str:
    '''
    Return the string representing the location of the proper texture file.
    '''
    # pick a random theme if none is specified
    if theme is None:
        theme = choice(list(Theme))

    if c == TileType.GROUND:
        return f"{theme.name.lower()}{typ.file_name('Ground')}"
    elif c == TileType.START:
        return "door_openMid"
    elif c == TileType.END:
        return "door_closedMid"
    elif c == TileType.START_TOP:
        return "door_openTop"
    elif c == TileType.END_TOP:
        return "door_closedTop"
    elif c == TileType.WATER:
        return f"liquidWater{typ.file_name('Water')}"