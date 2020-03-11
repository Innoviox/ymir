from visualizer.sprite.tile import Tile

class DeadlyTile(Tile):
    def collide(self, tile, direction, commit=True):
        if commit:
            self.controller.die()
        return False
