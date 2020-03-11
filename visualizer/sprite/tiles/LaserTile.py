from .MultidirectionalTile import MultidirectionalTile
from visualizer.sprite.util import Direction
from visualizer.constants import TileType
from itertools import starmap

def LaserTile(color):
    class _Laser(MultidirectionalTile):
        def setup(self):
            self.direction = super().setup().flip()

            self.on = True
            self.color = color
            self.laser = []

            curr = list(map(int, self.position))
            while True:
                curr[0] += self.direction.dx
                curr[1] += self.direction.dy

                t = self.controller.tile_at(*curr)
                if not t or t.type.is_ground():
                    break

                self.laser.append(t.position)

            self.toggle() # to load laser

        def toggle(self):
            for t in starmap(self.controller.tile_at, self.laser):
                if self.on:
                    if self.direction in [Direction.LEFT, Direction.RIGHT]:
                        t.load(TileType.LASER_HORIZ)
                        t.hitbox._hb = [0, 0.3, 1, 0.7]
                    else:
                        t.load(TileType.LASER_VERT)
                        t.hitbox._hb = [0.3, 0, 0.7, 1]
                    if not t.entity:
                        t.make_entity()
                    t.entity.show()
                    t.collide = lambda t, d, commit=True: commit and self.controller.die()
                    self.load(TileType.LASER_ON)
                else:
                    t.entity.hide()
                    t.collide = lambda t, d, commit=True: True
                    self.load(TileType.LASER_OFF)
    return _Laser