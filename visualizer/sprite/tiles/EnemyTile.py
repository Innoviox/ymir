from visualizer.sprite.tile import Tile
from visualizer.sprite.enemy import enemies

class EnemyTile(Tile):
    def setup(self):
        e = enemies[self.type.char](self.position, self.entity, self.controller, anim_texture=self.texture)

        self.controller.sprites.append(e)
