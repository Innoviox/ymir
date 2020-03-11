from visualizer.sprite.tile import Tile

class CheckpointTile(Tile):
    def collide(self, tile, direction, commit=True):
        if commit:
            self.load_toggle()
            if isinstance(self.controller.starting_tile, CheckpointTile):
                self.controller.starting_tile.load_toggle()
            self.controller.starting_tile = self
        return False
