import pygame as pg
import functools as ft
import os

pg.init()
screen = pg.display.set_mode((800, 600))

TEXTURES = {
    'O': None,
    'A': os.path.join('deluxe', 'grassCenter.png'),
    'a': os.path.join('deluxe', 'grassMid.png'),
    'S': os.path.join('deluxe', 'door_openMid.png'),
    's': os.path.join('deluxe', 'door_openTop.png'),
    'E': os.path.join('deluxe', 'door_closedMid.png'),
    'e': os.path.join('deluxe', 'door_closedTop.png'),
    'W': os.path.join('deluxe', 'liquidWater.png'),
    'w': os.path.join('deluxe', 'liquidWaterTop_mid.png'),
    'Player': os.path.join('characters', 'human', 'Adventurer', 'Poses', 'adventurer_idle.png')
}
BACKGROUND = (0, 0, 0) # black
SCALE = 0.5
SIZE = 70 # size of block
PLAYER_CENTER = (50, 50)

pg.sprite.Group.move_ip = lambda self, shift: [i.rect.move_ip(-shift[0], -shift[1]) for i in self.sprites()]

@ft.lru_cache(maxsize=len(TEXTURES))
def load_texture(file, scale=SCALE):
    img = pg.image.load(os.path.join('textures', file))
    if scale:
        img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    img = img.convert_alpha()
    return img

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, texture, t):
        super().__init__()
        self.image = load_texture(texture)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.collides = t in 'Aa'


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_texture(TEXTURES['Player'])
        self.rect = self.image.get_rect(center=PLAYER_CENTER)

        self.velocity = [0, 0] # x, y

        self.jumping = False
        self.in_air = False

    def handle(self, keys):
        self.dx = (-bool(keys[pg.K_LEFT]) + bool(keys[pg.K_RIGHT])) * 5
        # self.dy = (-bool(keys[pg.K_UP]) + bool(keys[pg.K_DOWN])) * 5
        if keys[pg.K_UP] and not self.jumping and not self.in_air:
            self.jumping = True
            self.dy = -12
            self.in_air = True
        elif self.jumping:
            self.dy += 1
        else:
            self.dy = 0

    @property
    def dx(self): return self.velocity[0]
    @dx.setter
    def dx(self, dx): self.velocity[0] = dx
    @property
    def dy(self): return self.velocity[1]
    @dy.setter
    def dy(self, dy): self.velocity[1] = dy


class Game:
    def __init__(self, file):
        self.tiles = pg.sprite.Group()
        with open(file) as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                for x, texture in enumerate(line.strip()):
                    if texture in 'AW':  # textures that modify when air is above them
                        if y > 0 and lines[y-1][x] == 'O':
                            texture = texture.lower()
                    if texture == 'S':
                        start_pos = (x * SIZE * SCALE, y * SIZE * SCALE)
                    t = TEXTURES[texture]
                    if t:
                        self.tiles.add(Tile(x * SIZE * SCALE, y * SIZE * SCALE, t, texture))

        self.tiles.move_ip([start_pos[0] - PLAYER_CENTER[0], start_pos[1] - PLAYER_CENTER[1] - 10])

        self.player = Player()

        self.clock = pg.time.Clock()

    def handle_player_collision(self):
        shift = [0, 0]
        bottom = False
        for tile in self.tiles.sprites():
            if tile.collides and self.player.rect.colliderect(tile.rect):
                if self.player.dx > 0 and tile.rect.left >= self.player.rect.left + 5 and abs(tile.rect.center[1] - self.player.rect.center[1]) <= 35:
                    shift[0] = tile.rect.left - self.player.rect.right
                    if abs(shift[0]) > 5: shift[0] = 0
                elif self.player.dx < 0 and tile.rect.right <= self.player.rect.left + 5 and abs(tile.rect.center[1] - self.player.rect.center[1]) <= 35:
                    shift[0] = tile.rect.right - self.player.rect.left
                    if abs(shift[0]) > 5: shift[0] = 0
                elif self.player.dy > 0 and tile.rect.bottom >= self.player.rect.top + 5 and abs(tile.rect.center[0] - self.player.rect.center[0]) <= 35:
                    shift[1] = tile.rect.top - self.player.rect.bottom
                    if abs(shift[1]) > 15: shift[1] = 0
                    else: bottom = True
                elif self.player.dy < 0 and tile.rect.top <= self.player.rect.bottom + 5 and abs(tile.rect.center[0] - self.player.rect.center[0]) <= 35:
                    shift[1] = tile.rect.bottom - self.player.rect.top
                    if abs(shift[1]) > 5: shift[1] = 0

            if tile.collides and tile.rect.top ==  self.player.rect.bottom and abs(tile.rect.center[0] - self.player.rect.center[0]) <= 35:
                bottom = True
                 
        self.player.in_air = not bottom
        self.player.jumping = not bottom
        self.tiles.move_ip(shift)

    def run(self):
        while True:
            self.clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            screen.fill(BACKGROUND)

            self.player.handle(pg.key.get_pressed())

            self.tiles.move_ip(self.player.velocity)
            self.handle_player_collision()
            self.tiles.update()
            self.tiles.draw(screen)

            screen.blit(self.player.image, self.player.rect)

            pg.display.flip()


if __name__ == '__main__':
    Game('test_file.txt').run()