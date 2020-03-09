from visualizer.sprite.tile import Tile, Hitbox
from visualizer.sprite.sprite import Sprite
from visualizer.sprite.util import Direction
from ursina import Sequence, Func

class SpringTile(Tile):
    def setup(self):
        self.hitbox = Hitbox([0, 0, 1, 0.5])

    def collide(self, tile, direction):
        if isinstance(tile, Sprite):
            if direction == Direction.UP:
                tile.velocity[1] = 3
                Sequence(Func(self.load_toggle), 1, Func(self.load_toggle)).start()
                return False
            return True
        return False
