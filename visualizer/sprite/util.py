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
    """Returns the magnitude of a list, interpreted as a numeric vector.""" 
    return math.sqrt(sum([x * x for x in a]))

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

def point_inside(point, position, hitbox):
    """Tells if a position is inside a tile."""
    x, y = position
    return x + hitbox.min_x < point[0] < x + hitbox.max_x and \
            y + hitbox.min_y < point[1] < y + hitbox.max_y

def collide(p, t, x=True, commit=False):
    """ Return the direction of Sprite (?) t relative to Sprite (?) p, depending on x.
            If x is false, return whether (the hitbox of) t is above p, below p, or neither.
            If x is true, return whether (the hitbox of) t is to the left of p, right of p, or neither.
            If commit is false, it's dry run collisions (e.g. colliding with a key will not unlock anything)"""
    chg = True
    direction = None
    if x:
        if t.x + t.hitbox.min_x < p.position[0] + p.hitbox.min_x < t.x + t.hitbox.max_x:
            if t.collide(p, Direction.LEFT, commit=commit):
                if commit:
                    p.position[0] = t.x + t.hitbox.max_x - p.hitbox.min_x
                direction = Direction.RIGHT
            else:
                chg = False
        elif t.x + t.hitbox.min_x < p.position[0] + p.hitbox.max_x < t.x + t.hitbox.max_x:
            if t.collide(p, Direction.RIGHT, commit=commit):
                if commit:
                    p.position[0] = t.x - (p.hitbox.max_x) #- p.hitbox.min_x)
                direction = Direction.LEFT
            else:
                chg = False
        else:
            chg = False
        if chg and commit:
            p.velocity[0] = 0
    else:
        if t.y + t.hitbox.min_y < p.position[1] + p.hitbox.min_y < t.y + t.hitbox.max_y:
            if t.collide(p, Direction.UP, commit=commit):
                if commit:
                    p.position[1] = t.y + t.hitbox.max_y
                    p.can_jump = True
                direction = Direction.DOWN
            else:
                chg = False
        elif t.y + t.hitbox.min_y < p.position[1] + p.hitbox.max_y < t.y + t.hitbox.max_y:
            if t.collide(p, Direction.DOWN, commit=commit):
                if commit:
                    p.position[1] = t.y - p.hitbox.max_y
                direction = Direction.UP
            else:
                chg = False
        else:
            chg = False
        if chg and commit:
            p.velocity[1] = 0

    return direction

