from enum   import Enum
from random import choice
from ursina import load_texture, compress_textures
from shutil import copyfile
from visualizer.tile import TileType

class GroundType(Enum):
    BOTTOM = 0
    TOP = 1
    LEFT = 2
    RIGHT = 3

class Theme(Enum):
    BLUE, BROWN, CASTLE, CHOCO, DIRT, GRASS, GREEN, METAL, PURPLE, SAND, SNOW, TUNDRA, YELLOW = range(13)

def load_ground_textures():
    for theme in Theme:
        for typ in GroundType:
            file = f"visualizer/assets/tiles/{theme.name.lower()}/{typ.name.lower()}.png"
            name = f"visualizer/textures/{theme.name.lower()}_{typ.name.lower()}.png"
            copyfile(file, name)
            # print(load_texture(name, file))

def texture(c: TileType, typ: GroundType, theme: Theme=None) -> str:
    '''
    Return the string representing the location of the proper texture file.
    '''
    # pick a random theme if none is specified
    if theme is None:
        theme = choice(list(Theme))

    if c == TileType.GROUND:
        return f"{theme.name.lower()}_{typ.name.lower()}"