from visualizer.sprite.tile import Tile, TileType
from visualizer.sprite.util import inside

class HorizontalMovingTile(Tile):
    def __init__(self, *args, **kwargs):
        hitbox = kwargs.pop("hitbox", [0.0, 0.5, 1.0, 1.0])
        super().__init__(*args, hitbox=hitbox, z_index=3)

        self.speed = 0.1
        self.offset = [0, 1]
        self.carry_with = True

    def update(self, dt):
        super().update(dt)

        self.entity.x += self.speed
        self.position[0] += self.speed

        if self.controller.next_is_ground(self, [self.offset[self.speed > 0], 0]):
            self.speed = -self.speed

        if self.carry_with:
            for entity in self.controller.sprites:
                if not entity.on_moving_tile and inside(entity.position + [0, -.1], self, hitbox=entity.hitbox):
                    entity.position[0] += self.speed
                    entity.velocity[1] = max(0, entity.velocity[1])
                    entity.on_moving_tile = self

    def set_offset(self, offset, total):
        if total == 1:
            return

        self.load(TileType.from_tile(f"N{'M' * (total - 2)},"[offset]))
        self.offset = [-offset, total - offset]

    # uncomment if you want to jump through moving platforms
    # def collide(self, tile, direction):
    #     return direction != Direction.DOWN
