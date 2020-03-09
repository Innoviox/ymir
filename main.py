import os
os.chdir('visualizer')

from visualizer import constants
constants.LEVEL = "visualizer"+constants.LEVEL[1:]
from visualizer.main import update, start
os.chdir('..')

start()