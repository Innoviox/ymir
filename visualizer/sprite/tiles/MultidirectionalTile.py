from visualizer.sprite.tile import Tile
from visualizer.sprite.util import Direction

class MultidirectionalTile(Tile):
    def setup(self):
        for (direction, rot) in zip(Direction, [0, 180, 270, 90]):
            if self.controller.next_is_ground(self, direction):
                self.entity.rotation_z = rot
                return direction