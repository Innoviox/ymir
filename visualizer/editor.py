from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.input_handler import held_keys

from visualizer.constants import TileType

class Item(Button):
    def __init__(self, editor, position, typ):
        self.tile_type = typ
        self.editor = editor

        super().__init__(model="quad",
                         texture=typ.texture(),
                         position=position,
                         scale=(0.05, 0.05, 0.05),
                         color=color.white)

    def on_click(self):
        if self.tile_type.texture():
            self.editor.current_paint.texture = self.tile_type.texture()
        else:
            self.editor.current_paint.texture = "white_cube"

class Voxel(Button):
    def __init__(self, editor, position):
        self.editor = editor
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
            self.texture = self.editor.current_paint.texture
        else:
            self.texture = 'white_cube'

dirs = {'w': [0, .1], 'a': [-.1, 0], 's': [0, -.1], 'd': [.1, 0]}

class Editor():
    def __init__(self):
        off_x = -.4
        off_y = .4
        x = 0
        y = 0
        self.menu_items = []
        for typ in TileType:
            self.menu_items.append(Item(self, (off_x+x, off_y+y), typ))
            x += .05

        self.grid = []
        for y in range(15):
            self.grid.append([])
            for x in range(20):
                self.grid[-1].append(Voxel(self, (x / 2, y / 2 - 1, 0)))

        self.current_paint = Entity(
            parent=scene,
            position=(-1, 0.5, -1),
            model='cube',
            origin_y=.5,
            texture=None,
            scale=0.5
        )

    def input(self, key):
        if key in dirs:
            for row in self.grid:
                for e in row:
                    e.x += dirs[key][0]
                    e.y += dirs[key][1]

        if key == 'left mouse up': # what the hell ursina
            held_keys['left mouse down'] = 0

    def update(self):
        pass

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