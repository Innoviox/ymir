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
                    tile_type = TileType.from_tile(tile)
                    if tile_type == TileType.GROUND:
                        if y > 0 and not level[y-1][x].type.is_ground():
                            tile_type = tile_type.toggle()
                    elif tile_type == TileType.WATER:
                        if y > 0 and not level[y-1][x].type.is_water():
                            tile_type = tile_type.toggle()

                    flipped_y = total - y - 1
                    level[y].append(tile_classes.get(tile, Tile)([x, flipped_y], tile_type, None))

                    if tile_type == TileType.MOVING:
                        level[y][-1].set_offset(m_count, m_count + len(line[x:]) - len(line[x:].lstrip(tile)))
                        m_count += 1
                    else:
                        m_count = 0
        return theme.split(","), level