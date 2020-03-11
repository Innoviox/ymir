from visualizer.sprite.tile import Tile
from ursina.input_handler import held_keys
from ursina import Sequence, Func
from visualizer.sprite.util import Hitbox
from collections import defaultdict

teleporter_locations = defaultdict(list)
teleporter_delay = 1 # teleporter delay in seconds

class TeleporterTile(Tile):
    teleported = False

    def setup(self):
        teleporter_locations[self.type.char].append(self.position)

    def collide(self, tile, direction, commit=True):
        if commit and 'Player' in str(type(tile)) and held_keys['s'] and not TeleporterTile.teleported:
            TeleporterTile.teleported = True
            Sequence(teleporter_delay, Func(self.set_teleported, False)).start()
            self.controller.player.position = [i for i in teleporter_locations[self.type.char] if i != self.position][0]
        return False

    def set_teleported(self, val):
        TeleporterTile.teleported = val