from .DeadlyTile import DeadlyTile
from .HorizontalMovingTile import HorizontalMovingTile
from visualizer.sprite.util import Direction

max_slicer_speed = 0.5
class SlicerTile(DeadlyTile, HorizontalMovingTile):
    def __init__(self, *args):
        super().__init__(*args)
        self.current_direction = Direction.RIGHT
        self.total = None
        self.carry_with = False

    def setup(self):
        super().setup()
        self.total = self.controller.next_ground(self, Direction.RIGHT)[0] + \
                     self.controller.next_ground(self, Direction.LEFT)[0]

    def update(self, dt):
        super().update()

        self.entity.rotation_z += self.speed * 20

        # speed is based on a quadratic curve - https://www.desmos.com/calculator/nclkc46nsd
        dist = self.controller.next_ground(self, self.current_direction)[0]
        self.speed = -(max_slicer_speed / ((self.total / 2) ** 2)) * dist * (dist - self.total) + 0.01

        if self.current_direction == Direction.LEFT:
            self.speed = -self.speed

        if dist < 0.2:
            self.current_direction = self.current_direction.flip()
