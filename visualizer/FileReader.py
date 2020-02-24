from visualizer.assets import texture, GroundType
from visualizer.tile import *


tile_map = {
    'O': TileType.AIR,
    'A': TileType.GROUND,
    'S': TileType.START,
    'E': TileType.END
}



class FileReader():
    def __init__(self, file_name):
        self.file_name = file_name
    '''
    returns 2D array with tiles
    '''
    def read(self):
        level = []
        with open(self.file_name,'r') as f:
            lines = f.readlines()
            for y,line in enumerate(lines):
                level.append([])
                for x,tile in enumerate(line):
                    if y > 0 and level[y-1][x].type == TileType.AIR:
                        type = GroundType.TOP
                    elif x > 0 and level[y][x-1].type == TileType.AIR:
                        type = GroundType.LEFT
                    else:
                        type = GroundType.bottom
                    level[y].append(Tile([x,y], texture(tile, type), tile_map[tile]))
                    if x < len(line) - 1 and level[y][x - 1].type == TileType.GROUND and level[y][x].type == TileType.AIR:
                        level[y][x-1].texture = texture(tile,GroundType.RIGHT)

        #flip the ys
        level = [[Tile([t.x,len(level) - t.position[1] - 1], tile.texture, tile.type) for t in line] for line in level]
        return level