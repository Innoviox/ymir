from .DeadlyTile import DeadlyTile
from visualizer.sprite.tile import Hitbox
from visualizer.sprite.util import Direction

spikes_hitboxes = [
    [0.0 , 0, 0.9, 0.25],
    [0.1, 0.75, 0.9, 1],
    [0.75, 0.1, 1, 0.9],
    [0, 0.1, 0.25, 0.9]
]


class SpikesTile(DeadlyTile):
    def __init__(self, *args):
        super().__init__(*args)

    def setup(self):
        super().setup()
        for (hb, direction, rot) in zip(spikes_hitboxes, Direction, [0, 180, 270, 90]):
            if self.controller.next_is_ground(self, direction):
                self.hitbox = Hitbox(hb)
                self.entity.rotation_z = rot
                return
