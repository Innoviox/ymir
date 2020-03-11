from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.input_handler import held_keys

from visualizer.constants import *

class Item(Button):
    def __init__(self, editor, position, typ):
        self.tile_type = typ
        self.editor = editor

        super().__init__(model="quad",
                         texture=typ.texture(anim=True),
                         position=position,
                         scale=(0.05, 0.05, 0.05),
                         color=color.white)

    def on_click(self):
        self.editor.current_paint_type = self.tile_type
        if self.tile_type.texture():
            self.editor.current_paint.texture = self.tile_type.texture(anim=True)
        else:
            self.editor.current_paint.texture = "white_cube"

class Voxel(Button):
    def __init__(self, editor, position):
        self.editor = editor
        self.tile_type = TileType.AIR
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(0, 0, 1),
            # highlight_color = color.lime,
            scale=0.5
        )

    def on_mouse_enter(self):
        self._update()

    def on_click(self):
        self._update(force=False)

    def _update(self, force=True):
        if force and not held_keys['left mouse down']:
            return
        if self.editor.current_paint.texture:
            self.tile_type = self.editor.current_paint_type
            self.texture = self.editor.current_paint.texture
        else:
            self.texture = 'white_cube'

        self.editor.save()

dirs = {'s': [0, .1], 'd': [-.1, 0], 'w': [0, -.1], 'a': [.1, 0]}

class Editor():
    def __init__(self):
        self.add_row_button = Button(
            parent=scene,
            position=(-0.5, 4, -1),
            origin_y=.5,
            on_click=self.add_row,
            text='+r'
        )

        self.add_col_button = Button(
            parent=scene,
            position=(2, 4, -1),
            origin_y=.5,
            on_click=self.add_col,
            text='+c'
        )

        off_x = -.4
        off_y = .4
        x = 0
        y = 0
        self.menu_items = []
        for typ in TileType:
            self.menu_items.append(Item(self, (off_x+x, off_y+y), typ))
            x += .05

        self.grid = []
        self.height = 15
        self.width = 20
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[-1].append(Voxel(self, (x / 2, y / 2 - 1, 0)))


        self.current_paint = Entity(
            parent=scene,
            position=(-1, 0.5, -1),
            model='cube',
            origin_y=.5,
            texture=None,
            scale=0.5
        )
        self.current_paint_type = TileType.AIR

    def input(self, key):
        if key == 'left mouse up': # what the hell ursina
            held_keys['left mouse down'] = 0
        if key.endswith('up'):
            held_keys[key[:-3]] = 0
        else:
            held_keys[key] = 1

    def update(self):
        for key in held_keys:
            if key in dirs and held_keys[key]:
                for row in self.grid:
                    for e in row:
                        e.x += dirs[key][0]
                        e.y += dirs[key][1]

    def save(self):
        file = "levels/save.txt"
        with open(file, "w") as f:
            f.write("None\n")
            for row in reversed(self.grid):
                for e in row:
                    f.write(e.tile_type.char)
                f.write("\n")

    def fix_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].position = (x / 2, y / 2 - 1, 0)

    def add_row(self):
        self.fix_grid()
        self.grid.append([])
        for x in range(self.width):
            self.grid[-1].append(Voxel(self, (x / 2, self.height / 2 - 1, 0)))
        self.height += 1

    def add_col(self):
        self.fix_grid()
        for y in range(self.height):
            self.grid[y].append(Voxel(self, ((self.width - 1) / 2, y / 2 - 1, 0)))
        self.width += 1

app = Ursina()

editor = Editor()

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'w')
input_handler.bind('down arrow', 's')

update = editor.update
input = editor.input
camera.position = (0, 0)

app.run()