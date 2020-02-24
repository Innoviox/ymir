from ursina import *
from Control import Controller
from Player import Player
import numpy as np

controller = Controller(Player(np.array([0,0],dtype='float64'),Entity(model="cube",color=color.blue)))

ground = Entity(model="cube", color = color.red)
ground.x = 0
ground.y = -1



def update():
    controller.update()

controller.start()