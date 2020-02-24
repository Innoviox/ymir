from enum   import Enum
from random import choice

class GroundType(Enum):
    BOTTOM = 0
    TOP = 1
    LEFT = 2
    RIGHT = 3

class Theme(Enum):
    BLUE, BROWN, CAKE, CASTLE, CHOCO, DIRT, GRASS, GREEN, METAL, PURPLE, SAND, SNOW, TUNDRA, YELLOW = range(14)

grounds = {
    'blue': ['3', '5', '4', '6'],

}

def file_for_char(c: str, typ: GroundType, theme: Theme=None) -> str:
    '''
    Tile mappings:
    G -> Ground
      -> Background.
    '''
    if theme is None:
        theme = choice(list(grounds.keys()))

    if c == 'G':
        return f"assets/tiles/{theme}/{}"
        # return f"assets/tiles/{theme}/tile{theme.title()}_{grounds[theme][typ.value].zfill(2)}.png"

print(file_for_char('G', GroundType.BOTTOM))