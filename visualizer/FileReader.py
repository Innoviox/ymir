'''
Read a level file, decode it into the necessary rendered tile objects.
'''
from visualizer.tile import *
from random import choice

class FileReader():
    def __init__(self, file_name):
        self.file_name = file_name
    '''
    returns 2D array of Tiles
    '''
    def read(self):
        level = []
        with open(self.file_name,'r') as f:
            lines = f.readlines()
            for y,line in enumerate(lines):
                level.append([])
                for x,tile in enumerate(line.strip()):
                    if tile == 'A':
                        if y > 0 and not level[y-1][x].type.is_ground():
                            tile = tile.lower()
                        # elif x > 0 and level[y][x-1].type != TileType.GROUND:
                        #     type = GroundType.LEFT
                    elif tile == 'W':
                        if y > 0 and not level[y-1][x].type.is_water():
                            tile = tile.lower()
                    level[y].append(Tile([x,y], TileType.from_tile(tile)))
                    # if x < len(line) - 1 and level[y][x - 1].type == TileType.GROUND and level[y][x].type != TileType.GROUND:
                    #     level[y][x-1].texture = assets.texture(tile_map[tile],GroundType.RIGHT, theme=theme)

        #flip the ys
        level = [[Tile([t.position[0],len(level) - t.position[1] - 1], t.type) for t in line] for line in level]
        return level