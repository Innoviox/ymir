'''
Read a level file, decode it into the necessary rendered tile objects.
'''
from visualizer.sprite.tile import *
from visualizer.sprite.tiles import tile_classes
from visualizer.constants import TileType

class FileReader():
    def __init__(self, file_name):
        self.file_name = file_name
    '''
    returns 2D array of Tiles
    '''
    def read(self):
        level = []
        with open(self.file_name,'r') as f:
            theme, *lines = f.readlines()
            total = len(lines)
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

                    flipped_y = total - y - 1
                    level[y].append(tile_classes.get(tile, Tile)([x, flipped_y], TileType.from_tile(tile), None))

                    if tile == 'M':
                        level[y][-1].set_offset(m_count, m_count + len(line[x:]) - len(line[x:].lstrip('M')))
                        m_count += 1
                    else:
                        m_count = 0
        return theme.split(","), level