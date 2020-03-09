from visualizer.sprite.tile import Tile
from visualizer.sprite.enemies import enemies

class EnemyTile(Tile):
    def setup(self):
        self.controller.sprites.append(enemies[self.type.char](self.position, self.type, self.controller))
        self.hide(now=True)