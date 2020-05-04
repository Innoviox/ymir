# Class built to be an attribute of the player class.
from math import floor
from random import random


class PlayerModel:

    def __init__(self):
        pass

    def choose_actions(self, sprites_on_screen):
        # process inputs and produce an action

        return [floor(random() + .5), floor(random() + .5), floor(random() + .5), floor(random() + .5)]
