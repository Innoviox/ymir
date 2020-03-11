from visualizer.sprite.tile import Tile
from ursina.input_handler import held_keys
from visualizer.sprite.util import Hitbox
class TeleporterTile(Tile):
    def setup(self):
        self.hitbox = Hitbox([0.4, 0.4, 0.6, 0.6])

    def collide(self, tile, direction, commit=True):
        # if commit and 'Player' in str(type(tile)):
        #     print(held_keys)
        #     print("teleporting")
        return False