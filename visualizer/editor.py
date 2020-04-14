from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.input_handler import held_keys

from visualizer.constants import *

"""Buttons for the various types of Tiles. Displayed at the top of the screen."""
class TileButton(Button):
    def __init__(self, editor, position, typ):
        self.tile_type = typ
        self.editor = editor

        super().__init__(model="quad",
                         texture=typ.default_texture(anim=True),
                         position=position,
                         scale=(0.05, 0.05, 0.05),
                         color=color.white)

    def on_click(self):
        self.editor.current_paint_type = self.tile_type
        if self.tile_type.default_texture():
            self.editor.current_paint.texture = self.tile_type.default_texture(anim=True)
        else:
            self.editor.current_paint.texture = "white_cube"

"""Represent locations on the grid that can be replaced with tiles. 
Initialized as white squares representing air spaces."""
class TilePlaceholder(Button):
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
        """Update tile when mouse is already pressed down and enters TilePlaceholder."""
        self._update()

    def on_click(self):
        """Update tile when TilePlaceholder is initially clicked."""
        self._update(force=False)

    def _update(self, force=True):
        """Change tile represented by the TilePlaceholder."""
        if force and not held_keys['left mouse down']:
            return
        if self.editor.current_paint.texture:
            self.tile_type = self.editor.current_paint_type
            self.texture = self.editor.current_paint.texture
        else:
            self.texture = 'white_cube'

        # auto-saves work :)
        self.editor.save()

dirs = {'s': [0, .1], 'd': [-.1, 0], 'w': [0, -.1], 'a': [.1, 0]}

class Editor():
    def __init__(self):
        # button to add more rows to the editable space
        self.add_row_button = Button(
            parent=scene,
            position=(-0.5, 4, -1),
            origin_y=.5,
            on_click=self.add_row,
            text='+r'
        )

        # button to add more columns to the editable space
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
        # Add all TileTypes (except air, I think?) as TileButtons, at offset positions on screen.
        for i, typ in enumerate(TileType, start=1):
            self.menu_items.append(TileButton(self, (off_x + x, off_y + y), typ))
            x += .05
            if i % 20 == 0:
                x = 0
                y -= .05

        self.grid = []
        self.height = 15
        self.width = 20
        self.create_grid()

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
        """A bodge to get around the fact that ursina's held_keys does not register when the left mouse button
        (and other buttons?) is/are no longer held."""
        print(key)
        if key == 'left mouse up':
            held_keys['left mouse down'] = 0
        # for any key event ending in 'up', force the key in the dict to be set to zero
        # TODO: May break when too many keys are held at once?
        if key.endswith('up'):
            held_keys[key[:-3]] = 0
        else:
            held_keys[key] = 1

    def update(self):
        "Move all the entities in the grid in the direction indicated by the held keys."
        for key in held_keys:
            if key in dirs and held_keys[key]:
                for row in self.grid:
                    for e in row:
                        e.x += dirs[key][0]
                        e.y += dirs[key][1]

    def save(self, file="levels/save.txt"):
        """Save the current level in the file <file>."""
        with open(file, "w") as f:
            f.write("None\n")
            for row in reversed(self.grid):
                for e in row:
                    f.write(e.tile_type.char)
                f.write("\n")

    def fix_grid(self):
        """Move grid items back to their original positions. (?)"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].position = (x / 2, y / 2 - 1, 0)

    def create_grid(self):
        """Delete the current grid variable and replace it with a new self.width
        by self.height grid of blank TilePlaceholders."""
        for r in self.grid:
            for j in r:
                destroy(j)
        self.grid = []
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[-1].append(TilePlaceholder(self, (x / 2, y / 2 - 1, 0)))

    def add_row(self):
        "Add a row of TilePlaceholders to the top of the grid."
        self.fix_grid()
        self.grid.append([])
        for x in range(self.width):
            self.grid[-1].append(TilePlaceholder(self, (x / 2, self.height / 2 - 1, 0)))
        self.height += 1

    def add_col(self):
        """Add a column of TilePlaceholders to the right side of the grid."""
        self.fix_grid()
        for y in range(self.height):
            self.grid[y].append(TilePlaceholder(self, ((self.width - 1) / 2, y / 2 - 1, 0)))
        self.width += 1

    def load_file(self, file):
        "Load file <file> into editor."
        with open(file) as f:
            theme, *k = list(f.readlines())
            self.height = len(k)
            self.width = len(k[0])
            self.create_grid()
            for i, line in enumerate(k):
                for j, tile in enumerate(line.strip()):
                    t = TileType.from_tile(tile)
                    if t.default_texture():
                        self.grid[self.height-i-1][j].tile_type = t
                        self.grid[self.height-i-1][j].texture = t.default_texture(anim=True)

app = Ursina()

editor = Editor()

# editor.load_file("./levels/test_file_3.txt")

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'w')
input_handler.bind('down arrow', 's')

update = editor.update
input = editor.input
camera.position = (0, 0)

app.run()