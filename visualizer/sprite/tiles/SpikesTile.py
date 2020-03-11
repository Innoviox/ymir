from .DeadlyTile import DeadlyTile
from .MultidirectionalTile import MultidirectionalTile
from visualizer.sprite.tile import Hitbox
from visualizer.sprite.util import Direction

spikes_hitboxes = [
    [0.0 , 0, 0.9, 0.25],
    [0.1, 0.75, 0.9, 1],
    [0.75, 0.1, 1, 0.9],
    [0, 0.1, 0.25, 0.9]
]


class SpikesTile(DeadlyTile, MultidirectionalTile):
    def setup(self):
        self.hitbox = Hitbox(spikes_hitboxes[super().setup().value])
