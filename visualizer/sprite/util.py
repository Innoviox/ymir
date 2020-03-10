import math
from enum import Enum

class Direction(Enum):
    UP, DOWN, RIGHT, LEFT = range(4)

    @property
    def diff(self):
        return [[0, -1], [0, 1], [1, 0], [-1, 0]][self.value]

    @property
    def dx(self):
        return self.diff[0]

    @property
    def dy(self):
        return self.diff[1]

    def flip(self):
        if self.value % 2 == 0:
            return Direction._value2member_map_[self.value + 1]
        return Direction._value2member_map_[self.value - 1]

def mag(a):
    """Returns the magnitude of an array, interpreted as a numeric vector.""" 
    return math.sqrt(sum([x * x for x in a]))


def inside(position, tile, density = 10): # todo: transparency (hitboxes)
    """Tells if an entity (anything with an ordered pair position vector) is inside the given tile.
    Works by testing the boundary points of the one by one box with the bottom left corner 
    in the specified position."""
    for i in range(density):
        if point_inside([position[0] + i / density, position[1]], tile):
            return True
        if point_inside([position[0] + i / density, position[1] + 1.0], tile):
            return True
        if point_inside([position[0], position[1] + i / density], tile):
            return True
        if point_inside([position[0] + 1.0, position[1] + i / density], tile):
            return True
    return False

def point_inside(point, tile):
    """Tells if a position is inside a tile."""
    return tile.x + tile.hitbox.min_x < point[0] < tile.x + tile.hitbox.max_x and \
            tile.y + tile.hitbox.min_y < point[1] < tile.y + tile.hitbox.max_y

def collide(p, t, x=True):
    chg = True
    direction = None
    out = False
    if 'Slime' in str(type(t)): out = True
    # out = False
    if out: print(x, p.position, t.position)
    if x:
        if t.x + t.hitbox.min_x < p.position[0] < t.x + t.hitbox.max_x:
            if out: print("\ta")
            if t.collide(p, Direction.LEFT):
                p.position[0] = t.x + t.hitbox.max_x
                direction = Direction.RIGHT
            else:
                chg = False
        elif t.x + t.hitbox.min_x < p.position[0] + t.hitbox.max_x < t.x + t.hitbox.max_x:
            if out: print("\tb")
            if t.collide(p, Direction.RIGHT):
                p.position[0] = t.x - t.hitbox.max_x
                direction = Direction.LEFT
            else:
                chg = False
        else:
            chg = False
        if chg:
            p.velocity[0] = 0
    else:
        if t.y + t.hitbox.min_y < p.position[1] < t.y + t.hitbox.max_y:
            if out: print("\tc")
            if t.collide(p, Direction.UP):
                p.position[1] = t.y + t.hitbox.max_y
                p.can_jump = True
                direction = Direction.DOWN
            else:
                chg = False
        elif t.y + t.hitbox.min_y < p.position[1] + t.hitbox.max_y < t.y + t.hitbox.max_y:
            if out: print("\td")
            if t.collide(p, Direction.DOWN):
                p.position[1] = t.y - t.hitbox.max_y
                direction = Direction.UP
            else:
                chg = False
        else:
            chg = False
        if chg:
            p.velocity[1] = 0

    return direction

TEXTURES = {
    'A': 'grassCenter',
    'O': None,
    'S': 'door_openMid',
    's': 'door_closedMid',
    'E': 'door_openTop',
    'e': 'door_closedTop',
    'W': 'liquidWater',
    'a': 'grassMid',
    'w': 'liquidWaterTop_mid',
    'M': 'grassHalfMid',
    'c': 'flagPole',
    'C': 'flagGreen',
    'P': 'spikes',
    'N': 'grassHalfLeft',
    ',': 'grassHalfRight',
    'K': 'keyBlue',
    'L': 'lockBlue',
    ';': 'keyRed',
    "'": 'lockRed',
    'Q': 'slicer',
    'G': 'slime',
    'B': 'enemyFlying',
    'r': 'spring',
    'R': 'sprung',
    '~': 'player'
}

texture_map = list(TEXTURES.values())
tile_map = ''.join(TEXTURES.keys())

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
    KEY_BLUE = 16
    LOCK_BLUE = 17
    KEY_RED = 18
    LOCK_RED = 19
    SLICER = 20
    SLIME = 21
    BUZZARD = 22
    SPRING_DOWN = 23
    SPRING_UP = 24
    PLAYER = 25

    def texture(self):
        return texture_map[self.value - 1]

    @classmethod
    def from_tile(cls, t):
        return cls._value2member_map_[tile_map.index(t) + 1]

    # todo: make better
    def is_ground(self): return self.value in [1, 8]
    def is_water(self): return self.value in [7, 9]

    def collides(self):
        return self.is_ground() or self.value in [17, 19]

    def player_collides(self):
        return self.value in [11, 13, 16, 18, 20, 23]

    def deadly(self):
        return self.value in [13, 20]

    def toggle(self):
        return TileType.from_tile(self.char.swapcase())

    def animatable(self):
        return self.value in [3, 4, 5, 6]

    def jump_through(self):
        return self.value in [10, 14, 15]

    @property
    def char(self):
        return tile_map[self.value - 1]

class Hitbox():
    def __init__(self, hb):
        self._hb = hb[:]

    @property
    def min_x(self): return self._hb[0]

    @property
    def min_y(self): return self._hb[1]

    @property
    def max_x(self): return self._hb[2]

    @property
    def max_y(self): return self._hb[3]