from visualizer.constants import TileType

jump_height = 5.0
jump_length = 8.0

class Level:
    def __init__(self, width, height, start_position):
        self.level = [[TileType.AIR for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

        self.level[start_position[1]][start_position[0]] = TileType.START
        self.level[start_position[1] - 1][start_position[0]] = TileType.START_TOP


