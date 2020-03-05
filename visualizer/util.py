import math
from visualizer import control
from visualizer.tile import TileType


def mag(a):
    """Returns the magnitude of an array, interpreted as a numeric vector.""" 
    return math.sqrt(sum([x * x for x in a]))


def inside(position, tile, density = 10):
    """Tells if an entity (anything with an ordered pair position vector) is inside the given tile.
    Works by testing the boundary points of the one by one box with the bottom left corner 
    in the specified position.""" 
    for i in range(0, density):
        if point_inside([position[0] + control.scale * i / density, position[1]], tile):
            return True
        if point_inside([position[0] + control.scale * i / density, position[1] + control.scale],
                        tile):
            return True
        if point_inside([position[0], position[1] + control.scale * i / density], tile):
            return True
        if point_inside([position[0] + control.scale, position[1] + control.scale * i / density],
                        tile):
            return True
    return False

def point_inside(point, tile):
    """Tells if a position is inside a tile."""
    if tile.x < point[0] < tile.x + control.scale and tile.y < point[1] < tile.y + control.scale:
        return True
    return False


def get_nearby_tiles(position, tile_array):
    """Return an array of the four tiles above, below, to the left and right of the position."""
    temp_position = position / control.scale
    temp_position[1] = len(tile_array) - temp_position[1] - 1
    a, b = int(temp_position[1]), int(temp_position[0])
    if 0 <= a < len(tile_array) and 0 <= b < len(tile_array[a]):
        yield tile_array[a][b]
    if 0 <= (a + 1) < len(tile_array) and 0 <= b < len(tile_array[a + 1]):
        yield tile_array[a + 1][b]
    if 0 <= a < len(tile_array) and 0 <= (b + 1) < len(tile_array[a]):
        yield tile_array[a][b + 1]
    if 0 <= (a + 1) < len(tile_array) and 0 <= (b + 1) < len(tile_array[a + 1]):
        yield tile_array[a + 1][b + 1]

def get_nearby_ground_tiles(position, tile_array):
    """Get all the adjacent tiles that are of type 'ground' (not air tiles)."""
    return list(filter(lambda x: x.type.collides(), get_nearby_tiles(position, tile_array)))

def collide(p, t, x=True):
    chg = True
    if x:
        if t.x + t.hitbox.min_x < p.position[0] < t.x + t.hitbox.max_x:
            p.position[0] = t.x + t.hitbox.max_x
        elif t.x + t.hitbox.min_x < p.position[0] + t.hitbox.max_x < t.x + t.hitbox.max_x:
            p.position[0] = t.x - t.hitbox.max_x
        else:
            chg = False
        if chg:
            p.velocity[0] = 0
    else:
        if t.y + t.hitbox.min_x < p.position[1] < t.y + t.hitbox.max_y:
            p.position[1] = t.y + t.hitbox.max_y
            p.can_jump = True
        elif t.y + t.hitbox.min_x < p.position[1] + t.hitbox.max_y < t.y + t.hitbox.max_y:
            p.position[1] = t.y - t.hitbox.max_y
        else:
            chg = False
        if chg:
            p.velocity[1] = 0
    return chg
