from visualizer.sprite.tile import Tile

class DeadlyTile(Tile):
    def collide(self, tile, direction):
        self.controller.die()
        return False
