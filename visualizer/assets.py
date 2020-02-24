from enum   import Enum
from random import choice

class GroundType(Enum):
    BOTTOM = 0
    TOP = 1
    LEFT = 2
    RIGHT = 3

class Theme(Enum):
    BLUE, BROWN, CASTLE, CHOCO, DIRT, GRASS, GREEN, METAL, PURPLE, SAND, SNOW, TUNDRA, YELLOW = range(13)

def texture(c: str, typ: GroundType, theme: Theme=None) -> str:
    '''
    Tile mappings:
    G -> Ground
      -> Background.
    '''
    if theme is None:
        theme = choice(list(Theme))

    file = None
    if c == 'G':
        file = f"assets/tiles/{theme.name.lower()}/{typ.name.lower()}.png"

        

