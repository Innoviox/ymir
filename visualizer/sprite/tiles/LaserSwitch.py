from visualizer.sprite.tile import Tile

class LaserSwitch(Tile):
    def collide(self, tile, direction, commit=True):
        return False