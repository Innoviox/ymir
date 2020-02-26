'''
Read a level file, decode it into the necessary rendered tile objects.
'''
from visualizer import assets
from visualizer.assets import GroundType, Theme
from visualizer.tile import *
from random import choice

tile_map = {
    'O': TileType.AIR,
    'A': TileType.GROUND,
    'S': TileType.START,
    'E': TileType.END,
    's': TileType.START_TOP,
    'e': TileType.END_TOP
}

class FileReader():
    def __init__(self, file_name):
        self.file_name = file_name
    '''
    returns 2D array of Tiles
    '''
    def read(self):
        level = []
        theme = Theme.GRASS
        with open(self.file_name,'r') as f:
            lines = f.readlines()
            for y,line in enumerate(lines):
                level.append([])
                for x,tile in enumerate(line.strip()):
                    if y > 0 and level[y-1][x].type != TileType.GROUND:
                        type = GroundType.TOP
                    elif x > 0 and level[y][x-1].type != TileType.GROUND:
                        type = GroundType.LEFT
                    else:
                        type = GroundType.BOTTOM
                    level[y].append(Tile([x,y], 
                        assets.texture(tile_map[tile], type, theme=theme), 
                        tile_map[tile]))
                    if x < len(line) - 1 and level[y][x - 1].type == TileType.GROUND and level[y][x].type != TileType.GROUND:
                        level[y][x-1].texture = assets.texture(tile_map[tile],GroundType.RIGHT, theme=theme)

        #flip the ys
        level = [[Tile([t.position[0],len(level) - t.position[1] - 1], t.texture, t.type) for t in line] for line in level]
        return level