from visualizer.assets import file_for_char, GroundType
from visualizer.tile import Tile

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
                    if y > 0 and level[y-1][x].type ==

                    level[y].append(Tile([x,y], file_for_char(tile, )))

