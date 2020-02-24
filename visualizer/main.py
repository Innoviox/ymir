from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app = Ursina() # Initialize application

# Set up window and camera
window.set_z_order(window.Z_top)
window.color = color.light_gray
window.size = (window.fullscreen_size[0]//2, window.fullscreen_size[1]//2)
window.position = (int(window.size[0]), int(window.size[1]-(window.size[1]/2)))
window.borderless = False
window.fullscreen = False
camera.orthographic = True
camera.fov = 20

def load_from_file(file):
    with open(file) as f:
        for y, line in enumerate(reversed(f.readlines())):
            for x, block in enumerate(line):
                if block == 'O': continue
                Entity(
                    model='cube',
                    color=color.dark_gray,
                    collider='box',
                    ignore=True,
                    position=(x, y),
                    scale=(1, 1)
                )
                print((x, y), block)

load_from_file("test_file.txt")

# Create player
player = PlatformerController2d(color=color.green.tint(-.3), position=(0, 10))
player.y = raycast(player.world_position, player.down).world_point[1]
camera.smooth_follow.offset[1] = 5

# Support arrow keys
input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')

app.run()
