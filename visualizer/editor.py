from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from visualizer.constants import TileType

class Item(Draggable):
    def __init__(self, position, typ):
        self.tile_type = typ

        super().__init__(model="quad",
                         texture=typ.texture(),
                         position=position,
                         scale=(0.05, 0.05, 0.05),
                         color=color.white)

    def on_click(self):
        print("clicked", self.type)

class Editor():
    def __init__(self):
        off_x = -.4
        off_y = .4
        x = 0
        y = 0
        self.menu_items = []
        for typ in TileType:
            self.menu_items.append(Item((off_x+x, off_y+y), typ))
            x += .05

        self.grid = []
        for y in range(5):
            self.grid.append([])
            for x in range(5):
                self.grid[-1].append(Entity(
                        parent = scene,
                        position=(x/2, y/2 - 1,0),
                        model = 'cube',
                        origin_y = .5,
                        texture = 'white_cube',
                        color = color.color(0, 0, random.uniform(.9, 1.0)),
                        # highlight_color = color.lime,
                        scale=0.5
                    ))

app = Ursina()

editor = Editor()

app.run()