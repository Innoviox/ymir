from .Enemy import Enemy

class BasicEnemy(Enemy):
    def __init__(self, *args, **kwargs):
        self.speed = kwargs.pop("speed") or 0.1

        super().__init__(*args, **kwargs)

        self.entity.double_sided = True

    def update(self, dt):
        super().update()
        self.velocity[0] = self.speed

    def update_collisions(self, tiles, tile_array):
        collided = super().update_collisions(tiles, tile_array)

        if Direction.LEFT in collided or Direction.RIGHT in collided:
            self.speed = -self.speed
            self.entity.rotation_y += 180

    def die(self):
        super().die()

        self.animator.kill()
        self.speed = 0
        self.entity.fade_out(duration=1, delay=1)

    def collide(self, tile, direction):
        if not self.dead and 'Player' in str(type(tile)): # hack to get around importing Player
            if direction == Direction.UP:
                tile.velocity[1] = tile.jump_speed
                tile.can_jump = False
                self.die()
            else:
                self.controller.die()
        return False
