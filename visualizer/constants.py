from enum import Enum

### Camera constants ###
scale = 1
camera_fov = 20
camera_offset = [0, 3, -30]
camera_speed = 2
OFFSET_X = 0
OFFSET_Y = 0

### Physics Constants ###
dt = .1
GRAVITY = -.5

LEVEL = "./levels/test_file_3.txt"
SKYBOX_PATHS = "./textures/Backgrounds"

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

    def default_texture(self, anim=False):
        if anim and self.value in [21, 22]:
            return texture_map[self.value - 1] + "_1"
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
