'''
Read a level file, decode it into the necessary rendered tile objects.
'''
from visualizer.sprite.tile import *

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
                m_count = 0
                for x,tile in enumerate(line.strip()):
                    if tile == 'A':
                        if y > 0 and not level[y-1][x].type.is_ground():
                            tile = tile.lower()
                        # elif x > 0 and level[y][x-1].type != TileType.GROUND:
                        #     type = GroundType.LEFT
                    elif tile == 'W':
                        if y > 0 and not level[y-1][x].type.is_water():
                            tile = tile.lower()
                    level[y].append(tile_classes.get(tile, Tile)([x, y], TileType.from_tile(tile), None))

                    if tile == 'M':
                        level[y][-1].set_offset(m_count, m_count + len(line[x:]) - len(line[x:].lstrip('M')))
                        m_count += 1
                    else:
                        m_count = 0

                    # if x < len(line) - 1 and level[y][x - 1].type == TileType.GROUND and level[y][x].type != TileType.GROUND:
                    #     level[y][x-1].texture = assets.texture(tile_map[tile],GroundType.RIGHT, theme=theme)

        #flip the ys
        # level = [[type(t)([t.position[0],len(level) - t.position[1] - 1], t.type, None) for t in line] for line in level]
        for i in level:
            for j in i:
                j.position[1] = len(level) - j.position[1] - 1

        return level