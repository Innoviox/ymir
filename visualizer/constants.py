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

# The key is the symbol that is used in the level files to represent the tile,
# The value is the name of the .png texture file
# Opposing states are represented by opposite case characters.
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
    '~': 'character',
    '1': 'teleporter1',
    '2': 'teleporter2'
}

texture_map = list(TEXTURES.values())
tile_map = ''.join(TEXTURES.keys())

# TODO remove pointless TileType enums (e.g. GROUND vs GROUND_TOP)
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
    TELEPORTER_1= 26
    TELEPORTER_2 = 27

    def default_texture(self, anim=False):
        """Return the file name of the default texture for the enum."""
        if anim and self.animatable():
            return texture_map[self.value - 1] + "_1"
        return texture_map[self.value - 1]

    @classmethod
    def from_tile(cls, t):
        """Given the character symbol of the texture, get the enum associated."""
        return cls._value2member_map_[tile_map.index(t) + 1]

    def is_ground(self): return self in [TileType.GROUND, TileType.GROUND_TOP]
    def is_water(self): return self in [TileType.WATER, TileType.WATER_TOP]

    def solid(self):
        """Can a sprite NOT pass through this tile?"""
        return self.is_ground() or self in [TileType.LOCK_BLUE, TileType.LOCK_RED,
                                            TileType.MOVING, TileType.MOVING_LEFT, TileType.MOVING_RIGHT]

    def player_collides(self):
        """Does something happen when the player collides with this tile?"""
        return self in [TileType.CHECKPOINT, TileType.SPIKES, TileType.KEY_BLUE,
                            TileType.KEY_RED, TileType.SLICER, TileType.SPRING_DOWN,
                        TileType.TELEPORTER_1, TileType.TELEPORTER_2]
    def deadly(self):
        """Does this tile kill the player on collision?"""
        return self in [TileType.SPIKES, TileType.SLICER]
    def animatable(self):
        """Does this tile have an associated Animator?"""
        return self in [TileType.SLIME, TileType.BUZZARD]
    def jump_through(self):
        """Can the player jump through the bottom of this tile?"""
        return self in [TileType.MOVING, TileType.MOVING_LEFT, TileType.MOVING_RIGHT]
   
    def toggle(self):
        """Return the TileType enum of the opposite state 
        (the one associated with the opposite case character symbol)."""
        return TileType.from_tile(self.char.swapcase())

    @property
    def char(self):
        """Given an enum, get the associated character symbol."""
        return tile_map[self.value - 1]
