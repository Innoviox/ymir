from enum   import Enum
from random import choice

class GroundType(Enum):
    BOTTOM = 0
    TOP = 1
    LEFT = 2
    RIGHT = 3

class Theme(Enum):
    BLUE, BROWN, CASTLE, CHOCO, DIRT = range(5)
        #, DIRT, GRASS, GREEN, METAL, PURPLE, SAND, SNOW, TUNDRA, YELLOW = range(13)

def file_for_char(c: str, typ: GroundType, theme: Theme=None) -> str:
    '''
    Tile mappings:
    G -> Ground
      -> Background.
    '''
    if theme is None:
        theme = choice(list(Theme))

    if c == 'G':
        return f"assets/tiles/{theme.name.lower()}/{typ.name.lower()}.png"

print(file_for_char('G', GroundType.BOTTOM))