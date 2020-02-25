from ursina import *
from visualizer.control import Controller
from visualizer.player import Player
import numpy as np

controller = Controller(Player(np.array([0,0],dtype='float64'),
	Entity(model="cube",color=color.blue,scale=1)))

def update():
    controller.update()

controller.start()