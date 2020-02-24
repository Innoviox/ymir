from enum   import Enum
from random import choice
from ursina import load_texture
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
            file = f"assets/tiles/{theme.name.lower()}/{typ.name.lower()}.png"
            load_texture(f"{theme.name.lower()}_{typ.name.lower()}", file)

def texture(c: str, typ: GroundType, theme: Theme=None) -> str:
    '''
    Tile mappings:
    G -> Ground
      -> Background.
    '''
    if theme is None:
        theme = choice(list(Theme))

    if c == 'G':
        return f"{theme.name.lower()}_{typ.name.lower()}"