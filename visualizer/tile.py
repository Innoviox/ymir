'''
Create a 'Tile' object with type and (x,y) location. 
'''
from visualizer import util
from visualizer.util import *
from visualizer import enemy
from visualizer.player import Player

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
    'C': 'flagGreen_up',
    'P': 'spikes',
    'N': 'grassHalfLeft',
    ',': 'grassHalfRight',
    'K': 'keyBlue',
    'L': 'lockBlue',
    ';': 'keyRed',
    "'": 'lockRed',
    'Q': 'slicer',
    'G': 'slime_1'
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

    def texture(self):
        return texture_map[self.value - 1]

    @classmethod
    def from_tile(cls, t):
        return cls._value2member_map_[tile_map.index(t) + 1]

    # todo: make better
    def is_ground(self): return self.value in [1, 8]
    def is_water(self): return self.value in [7, 9]

    def collides(self):
        return self.is_ground() or self.value in [11, 13, 16, 17, 18, 19, 20]

    def deadly(self):
        return self.value in [13, 20]

    def toggle(self):
        return TileType.from_tile(self.char.swapcase())

    def animatable(self):
        return self.value in [3, 4, 5, 6]

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
HITBOX=[0.0, 0.0, 1.0, 1.0]

class Tile():
    def __init__(self, position, typ, controller, hitbox=HITBOX): # hitbox: min-x, min-y, max-x, max-y
        self.position = position
        self.hitbox = Hitbox(hitbox[:])

        self.type = typ
        self.texture = self.type.texture()
        self.entity = None
        self.controller = controller

        # self.animator = Animator(self, f"{TEXTURES[t.upper()]}_to_{TEXTURES[t.lower()]}_slice_")
        # self.anim_dir = [-1, 1][self.type.char.isupper()]
        # self.anim_frame = 0
        # self.animating = False
        # self.anim_every = 1
        # self.anim_step = 0

    def load(self, new_type, texture=True):
        self.type = new_type
        self.texture = self.type.texture()
        if self.entity and texture:
            self.entity.texture = self.texture

    def load_toggle(self): self.load(self.type.toggle())

    def update(self):
        ...
        # if self.type.animatable() and self.animating:
        #     self.anim_step += 1
        #     if self.anim_step % self.anim_every == 0:
        #         self.anim_toggle()

    def collide(self, tile):
        return True  # if this method is called, then self.type.collides()

    @property
    def x(self):
        return self.position[0]
    @property
    def y(self):
        return self.position[1]

    def __repr__(self):
        return str(self.type).split(".")[1]# + " at " + str(self.position)

    def anim_toggle(self): # note: toggleanim files go from upper -> lower
        ...
        # self.anim_frame += 1
        # if self.anim_frame == 70:
        #     self.load(self.type.toggle())
        #     self.animating = False
        # else:
        #     t = tile_map[self.type.value - 1]
        #     self.entity.texture = f"{self.anim_frame}"

    def hide(self, now=False):
        self.type = TileType.AIR
        if now:
            self.entity.hide()
        else:
            self.entity.fade_out()

    def setup(self):
        ...

def HitboxTile(hitbox):
    class _T(Tile):
        def __init__(self, *args):
            super().__init__(*args, hitbox=hitbox)

    return _T

class HorizontalMovingTile(Tile):
    def __init__(self, *args):
        super().__init__(*args, hitbox=[0.0, 0.5, 1.0, 1.0])

        self.speed = 0.1
        self.offset = [0, 1]
        self.carry_with = True

    def update(self):
        super().update()

        self.entity.x += self.speed
        self.position[0] += self.speed

        if self.controller.next_is_ground(self, [self.offset[self.speed > 0], 0]):
            self.speed = -self.speed

        if self.carry_with:
            for entity in self.controller.sprites:
                if not entity.on_moving_tile and util.inside(entity.position + [0, -.1], self):
                    entity.position[0] += self.speed
                    entity.on_moving_tile = self

    def set_offset(self, offset, total):
        if total == 1:
            return

        self.load(TileType.from_tile(f"N{'M' * (total - 2)},"[offset]))
        self.offset = [-offset, total - offset]

class CheckpointTile(Tile):
    def collide(self, tile):
        if not isinstance(tile, Player):
            return False # todo: collide with nonplayer? (eg drop a box on it)
        self.load_toggle()
        if isinstance(self.controller.starting_tile, CheckpointTile):
            self.controller.starting_tile.load_toggle()
        self.controller.starting_tile = self
        return False

class KeyTile(Tile):
    def collide(self, tile):
        if not isinstance(tile, Player):
            return False
        self.controller.unlock(self.type)
        self.hide(now=True)
        return False

spikes_hitboxes = [
    [0.1, 0, 0.9, 0.25],
    [0.1, 0.75, 0.9, 1],
    [0.85, 0.1, 1, 0.9],
    [0, 0.1, 0.15, 0.9]
]

class DeadlyTile(Tile):
    def collide(self, tile):
        if not isinstance(tile, Player):
            return False
        self.controller.die()
        return False

class SpikesTile(DeadlyTile):
    def __init__(self, *args):
        super().__init__(*args)

    def setup(self):
        super().setup()
        for (hb, direction, rot) in zip(spikes_hitboxes, Direction, [0, 180, 270, 90]):
            if self.controller.next_is_ground(self, direction):
                self.hitbox = Hitbox(hb)
                self.entity.rotation_z = rot
                return


max_slicer_speed = 0.5
class SlicerTile(HorizontalMovingTile, DeadlyTile):
    def __init__(self, *args):
        super().__init__(*args)
        self.current_direction = Direction.RIGHT
        self.total = None
        self.carry_with = False

    def setup(self):
        super().setup()
        self.total = self.controller.next_ground(self, Direction.RIGHT)[0] + \
                     self.controller.next_ground(self, Direction.LEFT)[0]

    def update(self):
        super().update()

        self.entity.rotation_z += self.speed * 20

        # speed is based on a quadratic curve - https://www.desmos.com/calculator/nclkc46nsd
        dist = self.controller.next_ground(self, self.current_direction)[0]
        self.speed = -(max_slicer_speed / ((self.total / 2) ** 2)) * dist * (dist - self.total) + 0.01

        if self.current_direction == Direction.LEFT:
            self.speed = -self.speed

        if dist < 0.2:
            self.current_direction = self.current_direction.flip()

class EnemyTile(Tile):
    def setup(self):
        self.controller.sprites.append(enemy.enemies[self.type.char](self.position, self.entity))

tile_classes = {'M': HorizontalMovingTile, 'c': CheckpointTile, 'P': SpikesTile,
                'K': KeyTile, ';': KeyTile,
                'Q': SlicerTile,
                'G': EnemyTile}